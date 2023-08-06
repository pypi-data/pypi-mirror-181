import os
import sys
from typing import Union

import requests
from suds.client import Client
from suds.transport import Reply
from suds.transport.http import HttpAuthenticated

if 'komle_witslm_client.bindings.v1411.write' in sys.modules:
    # Witsml uses the same namespace for each schema
    # So for now check what binding is in use
    from komle_witslm_client.bindings.v1411.write import witsml
else:
    # Default to import read_bindings
    from komle_witslm_client.bindings.v1411.api import witsml as cap_server
    from komle_witslm_client.bindings.v1411.read import witsml


class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self.verify = kwargs.pop('verify', None)
        self.auth = (
            kwargs.pop("username", None),
            kwargs.pop("password", None),
        )
        HttpAuthenticated.__init__(self, **kwargs)

    def send(self, request):
        resp = requests.post(
            request.url,
            data=request.message,
            headers=request.headers,
            verify=self.verify,
            auth=self.auth,
        )
        resp.raise_for_status()
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result


def simple_client(
    service_url: str,
    username: str,
    password: str,
    agent_name: str = "komle-plus",
    verify: Union[bool, str] = True,
) -> Client:
    """Create a simple soap client using Suds,

    This initializes the client with a local version of WMLS.WSDL 1.4 from energistics.

    Args:
        service_url (str): url giving the location of the Store
        username (str): username on the service
        password (str): password on the service
        agent_name (str): User-Agent name to pass in header
        verify (bool|str): Whether to verify TLS certificates, or path to a cacerts file

    Returns:
        client (Client): A suds client with wsdl
    """

    transport = RequestsTransport(username=username, password=password, verify=verify)

    client = Client(
        f'file:{os.path.join(os.path.dirname(__file__), "WMLS.WSDL")}',
        location=service_url,
    )

    client.set_options(transport=transport, headers={"User-Agent": agent_name})

    return client


class StoreException(Exception):
    def __init__(self, reply):
        super().__init__(
            f" WITSMLStoreError -> Result: {reply.Result} SuppMsgOut: {reply.SuppMsgOut}"
        )
        self.reply = reply


def _parse_reply(reply):
    if reply.Result == 1 or reply.Result == 2 or reply.SuppMsgOut == "Function completed successfully":
        return witsml.CreateFromDocument(reply.XMLout)
    else:
        raise StoreException(reply)


class StoreClient:
    def __init__(
        self,
        service_url: str,
        username: str,
        password: str,
        agent_name: str = "komle-plus",
        verify: Union[bool, str] = True,
    ):
        """Create a GetFromStore client,

        This initializes the client with a local version of WMLS.WSDL 1.4 from energistics.

        Args:
            service_url (str): url giving the location of the Store
            username (str): username on the service
            password (str): password on the service
            agent_name (str): User-Agent name to pass in header
            verify (bool|str): Whether to verify TLS certificates, or path to a cacerts file
        """

        self.soap_client = simple_client(
            service_url, username, password, agent_name, verify
        )

    def get_bhaRuns(
        self,
        q_bha: witsml.obj_bhaRun,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.bhaRuns:
        """Get bhaRuns from a witsml store server

        The default is only to return id-only, change to all when you know what bhaRun to get.


        Args:
            q_bha (witsml.obj_bhaRun): A query bhaRun specifing objects to return, can be an empty bhaRun
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
            OptionsIn (str): String describing more options [cascadedDelete, dataVersion]
        Returns:
            witsml.bhaRuns: bhaRuns a collection of bhaRun

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_bhas = witsml.bhaRuns(version=witsml.__version__)

        q_bhas.append(q_bha)

        reply_bhas = self.soap_client.service.WMLS_GetFromStore(
            "bhaRun",
            q_bhas.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_bhas)

    def get_cap(
        self, dataVersion: str, OptionsIn: str = ""
    ) -> cap_server.obj_capServers:
        """Get capabilities from a witsml store server.

        Args:
            dataVersion (str): Define the version witsml use in capServers

        Returns:
            cap_server.obj_capServers: capServers a collection of capServer

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """
        reply_cap = self.soap_client.service.WMLS_GetCap(
            "cap",
            OptionsIn=f"dataVersion={dataVersion};{OptionsIn}",
        )
        reply_new = (
            reply_cap.CapabilitiesOut.replace("131", "141")
            .replace("1.3.1", "1.4.1")
            .replace("1.3.1.1", "1.4.1.1")
            .replace("></", ">None</")
        )
        return cap_server.CreateFromDocument(reply_new)

    def get_logs(
        self,
        q_log: witsml.obj_log,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.logs:
        """Get logs from a witsml store server

        The default is to return id-only, change to all when you know what log to get.
        Pass an empty log with returnElements id-only to get all by id.


        Args:
            q_log (witsml.obj_log): A query log specifing objects to return, for example uidWell, uidWellbore or an empty log
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.logs: logs a collection of log

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_logs = witsml.logs(version=witsml.__version__)

        q_logs.append(q_log)

        reply_logs = self.soap_client.service.WMLS_GetFromStore(
            "log",
            q_logs.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_logs)

    def get_mudLogs(
        self,
        q_mudlog: witsml.obj_mudLog,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.mudLogs:
        """Get mudLogs from a witsml store server

        The default is only to return id-only, change to all when you know what mudLog to get.
        Pass an empty mudLog with returnElements id-only to get all by id.


        Args:
            q_mudlog (witsml.obj_mudLog): A query mudLog specifing objects to return, can be empty
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.mudLogs: mudLogs, a collection of mudLog

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_mudlogs = witsml.mudLogs(version=witsml.__version__)

        q_mudlogs.append(q_mudlog)

        reply_mudlogs = self.soap_client.service.WMLS_GetFromStore(
            "mudLog",
            q_mudlogs.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_mudlogs)

    def get_trajectorys(
        self,
        q_traj: witsml.obj_trajectory,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.trajectorys:
        """Get trajectorys from a witsml store server

        The default is only to return id-only, change to all when you know what trajectory to get.
        Pass an empty trajectory with returnElements id-only to get all by id.

        Args:
            q_traj (witsml.obj_trajectory): A query trajectory specifing objects to return
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.trajectorys: trajectorys, a collection of trajectory

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_trajs = witsml.trajectorys(version=witsml.__version__)

        q_trajs.append(q_traj)

        reply_traj = self.soap_client.service.WMLS_GetFromStore(
            "trajectory",
            q_trajs.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_traj)

    def get_version(self) -> list:
        """Get version from a witsml store server

        Returns:
            list: version

        Raises:
            StoreException: If the soap server replies with an error
        """
        reply_version = self.soap_client.service.WMLS_GetVersion(
            "version",
            OptionsIn="returnElements=None",
        )

        return reply_version.split(",")

    def get_wellbores(
        self,
        q_wellbore: witsml.obj_wellbore,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.wellbores:
        """Get wellbores from a witsml store server

        The default is only to return id-only, change to all when you know what wellbore to get.


        Args:
            q_wellbore (witsml.obj_wellbore): A query wellbore specifing objects to return, can be an empty wellbore
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.wellbores: wellbores

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_wellbores = witsml.wellbores(version=witsml.__version__)

        q_wellbores.append(q_wellbore)

        reply_wellbores = self.soap_client.service.WMLS_GetFromStore(
            "wellbore",
            q_wellbores.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_wellbores)

    def get_wells(
        self,
        q_well: witsml.obj_well,
        returnElements: str = "id-only",
        OptionsIn: str = "",
    ) -> witsml.wells:
        """Get wells from a witsml store server

        The default is only to return id-only, change to all when you know what well to get.


        Args:
            q_well (witsml.obj_well): A query well specifing objects to return, can be an empty well
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.wells: wells

        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        """

        q_wells = witsml.wells(version=witsml.__version__)

        q_wells.append(q_well)

        reply_wells = self.soap_client.service.WMLS_GetFromStore(
            "well",
            q_wells.toxml(),
            OptionsIn=f"returnElements={returnElements};{OptionsIn}",
        )

        return _parse_reply(reply_wells)

    def get_rigs(
        self, 
        q_rig: witsml.obj_rig,
        returnElements: str='id-only',
        OptionsIn: str = "",
    ) -> witsml.rigs:
        '''Get Rigs from a witsml store server
    
        The default is only to return id-only, change to all when you know what rig to get.
    
    
        Args:
            q_rig (witsml.obj_rig): A query rig specifing objects to return, can be an empty rig
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.rigs: rigs
        
        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        '''
    
        q_rigs = witsml.rigs(version=witsml.__version__)
    
        q_rigs.append(q_rig)
    
        reply_rigs = self.soap_client.service.WMLS_GetFromStore(
            'rig',
            q_rigs.toxml(),
            OptionsIn=f'returnElements={returnElements};{OptionsIn}',
        )
    
        return _parse_reply(reply_rigs)

    def get_wbGeometrys(
        self, 
        q_wbGeometry: witsml.obj_wbGeometry,
        returnElements: str='id-only',
        OptionsIn: str = "",
    ) -> witsml.wbGeometrys:
        '''Get wbGeometry from a witsml store server
    
        The default is only to return id-only, change to all when you know what wbGeometry to get.
    
    
        Args:
            q_wbGeometry (witsml.obj_wbGeometry): A query wbGeometry specifing objects to return, can be an empty wbGeometry
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.wbGeometrys: wbGeometrys
        
        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        '''
    
        q_wbGeometrys = witsml.wbGeometrys(version=witsml.__version__)
    
        q_wbGeometrys.append(q_wbGeometry)
    
        reply_wbGeometrys = self.soap_client.service.WMLS_GetFromStore(
            'wbGeometry',
            q_wbGeometrys.toxml(),
            OptionsIn=f'returnElements={returnElements};{OptionsIn}',
        )
    
        return _parse_reply(reply_wbGeometrys)

    def get_tubulars(
        self, 
        q_tubular: witsml.obj_tubular,
        returnElements: str='id-only',
        OptionsIn: str = "",
    ) -> witsml.tubulars:
        '''Get Tubulars from a witsml store server
    
        The default is only to return id-only, change to all when you know what tubular to get.
    
    
        Args:
            q_tubular (witsml.obj_tubular): A query rig specifing objects to return, can be an empty tubular
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.tubulars: tubulars
        
        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        '''
    
        q_tubulars = witsml.tubulars(version=witsml.__version__)
    
        q_tubulars.append(q_tubular)
    
        reply_tubulars = self.soap_client.service.WMLS_GetFromStore(
            'tubular',
            q_tubulars.toxml(),
            OptionsIn=f'returnElements={returnElements};{OptionsIn}',
        )
    
        return _parse_reply(reply_tubulars)

    def get_stimJobs(
        self, 
        q_stimJob: witsml.obj_stimJob,
        returnElements: str='id-only',
        OptionsIn: str = "",
    ) -> witsml.stimJobs:
        '''Get StimJobs from a witsml store server
    
        The default is only to return id-only, change to all when you know what StimJob to get.
    
    
        Args:
            q_stimJob (witsml.obj_stimJob): A query rig specifing objects to return, can be an empty StimJob
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.stimJobs: stimJobs
        
        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        '''
    
        q_stimJobs= witsml.stimJobs(version=witsml.__version__)
    
        q_stimJobs.append(q_stimJob)
    
        reply_stimJobs = self.soap_client.service.WMLS_GetFromStore(
            'stimJob',
            q_stimJobs.toxml(),
            OptionsIn=f'returnElements={returnElements};{OptionsIn}',
        )
        # print(reply_stimJobs)
        return _parse_reply(reply_stimJobs)


    def get_cementJobs(
        self, 
        q_cementJob: witsml.obj_cementJob,
        returnElements: str='id-only',
        OptionsIn: str = "",
    ) -> witsml.cementJobs:
        '''Get CementJobs from a witsml store server
    
        The default is only to return id-only, change to all when you know what CementJob to get.
    
    
        Args:
            q_cementJob (witsml.obj_cementJob): A query rig specifing objects to return, can be an empty CementJob
            returnElements (str): String describing data to get on of [all, id-only, header-only, data-only, station-location-only
                                                                       latest-change-only, requested]
        Returns:
            witsml.cementJobs: cementJobs
        
        Raises:
            StoreException: If the soap server replies with an error
            pyxb.exception: If the reply is empty or the document fails to validate a pyxb exception is raised
        '''
    
        q_cementJobs = witsml.cementJobs(version=witsml.__version__)
    
        q_cementJobs.append(q_cementJob)
    
        reply_cementJobs = self.soap_client.service.WMLS_GetFromStore(
            'cementJob',
            q_cementJobs.toxml(),
            OptionsIn=f'returnElements={returnElements};{OptionsIn}',
        )
    
        return _parse_reply(reply_cementJobs)