# -*- coding: utf-8 -*-
import numpy as np
import pickle
import shutil
import time
import os
import pathlib
from joblib import Parallel, delayed
from typing import List
from termcolor import colored


def create_message_file(path: pathlib.PosixPath):
    file = open(path, "wb")
    file.close()

def remove_message_file(path: pathlib.PosixPath):
    os.remove(path)

def get_files_in_folder(dir_path: pathlib.PosixPath):
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(dir_path.joinpath(path)):
            res.append(path)
    return res

def log_print(text, color, end = '\n'):
    '''Description: Colorful printing.

    Args:
        text:  'str' type, the string to print.
        color: 'str' type, text color.
    '''

    if color == 'r':
        print(colored(text, 'red'), end = end)
    elif color == 'g':
        print(colored(text, 'green'), end = end)
    elif color == 'b':
        print(colored(text, 'blue'), end = end)
    elif color == 'y':
        print(colored(text, 'yellow'), end = end)
    elif color == 'c':
        print(colored(text, 'cyan'), end = end)
    elif color == 'm':
        print(colored(text, 'magenta'), end = end)
    else:
        print(text, end = end)


class ClientObject:
    def __init__(self):
        self.__id_number = -1
        self.__client_cache_folder = -1
        self.__project_metadata_cache_path = -1
        self.__server_to_connect_id = -1

    def _initialize(self,
    client_id: int,
    server_to_connect_id: int,
    meta_data: dict,
    project_metadata_cache_path: pathlib.PosixPath,
    ) -> bool:
        self.__id_number = client_id
        self.__project_metadata_cache_path = project_metadata_cache_path
        self.__server_to_connect_id = server_to_connect_id
        self.__comm_cache_folder = self.__project_metadata_cache_path.joinpath(str(self.__server_to_connect_id))
        self.__client_cache_folder = self.__comm_cache_folder.joinpath(str(self.__id_number))

        # Create client cache folder
        if os.path.exists(self.__client_cache_folder):
            shutil.rmtree(self.__client_cache_folder)
            os.mkdir(self.__client_cache_folder)
        else:
            os.mkdir(self.__client_cache_folder)

        meta_data = {self.__id_number: meta_data}
        file = open(self.__client_cache_folder.joinpath('meta_data.pkl'), "wb")
        pickle.dump(meta_data, file)
        file.close()

        # Print initialization info
        log_print('+-------------------------- Client Initialization Finished --------------------------+', 'g')
        log_print('+---> Client ID: %d' % self.__id_number, 'g')
        log_print('+---> Server to connect ID: %d' % self.__server_to_connect_id, 'g')
        log_print('+------------------------------------------------------------------------------------+', 'g')

        return True

    def _get_client_id(self) -> int:
        return self.__id_number

    def _get_server_to_connect_id(self) -> int:
        return self.__server_to_connect_id
    
    def __request_connect_to_server(self) -> bool:
        create_message_file(self.__comm_cache_folder.joinpath('connect_requesting', str(self.__id_number)))
        return True

    def __is_connected_to_server(self) -> bool:
        if os.path.exists(self.__comm_cache_folder.joinpath('connected', str(self.__id_number))):
            return True
        else:
            return False

    def __is_selected(self) -> bool:
        if os.path.exists(self.__comm_cache_folder.joinpath('round_selected', str(self.__id_number))):
            return True
        else:
            return False

    def local_update(self, global_model_parameters: List) -> tuple:
        layermask_vector = np.ones_like(36)
        local_model_updates = [np.ones_like(global_model_parameters[layer_idx]*layermask_vector[layer_idx]) for layer_idx in range(len(global_model_parameters))]
        time.sleep(20)
        return local_model_updates, layermask_vector
    
    def __local_update(self) -> bool:
        # Load global model parameters
        file = open(self.__comm_cache_folder.joinpath('global_model_parameters.pkl'), "rb")
        last_round_global_model_parameters = pickle.load(file)
        file.close()

        # Local update
        local_model_updates, layermask_vector = self.local_update(last_round_global_model_parameters)

        assert len(local_model_updates) == len(last_round_global_model_parameters)
        for layer_idx in range(len(last_round_global_model_parameters)):
            assert last_round_global_model_parameters[layer_idx].shape == local_model_updates[layer_idx].shape
        
        file = open(self.__client_cache_folder.joinpath('local_updates.pkl'), "wb")
        pickle.dump({self.__id_number: local_model_updates}, file)
        file.close()

        file = open(self.__client_cache_folder.joinpath('layermask.pkl'), "wb")
        pickle.dump({self.__id_number: layermask_vector}, file)
        file.close()

        remove_message_file(self.__comm_cache_folder.joinpath('round_selected', str(self.__id_number)))

    def _start(self) -> bool:
        while self.__is_connected_to_server() == False:
            log_print("[Client %d Info] Server not connected..." % self.__id_number, color = 'm')
            self.__request_connect_to_server()
            time.sleep(3)

        log_print("[Client %d Info] Server successfully connected" % self.__id_number, color = 'g')
        
        while os.path.exists(self.__comm_cache_folder.joinpath('exit')) == False:
            if self.__is_selected():
                log_print("[Client %d Info] Be selected to participate in the update and begin local update..." % self.__id_number, color = 'm')
                self.__local_update()
                log_print("[Client %d Info] Local update finished!" % self.__id_number, color = 'g')
        log_print("[Client %d Info] Training finished!" % self.__id_number, color = 'b')
        return True


class ServerObject:
    def __init__(self):
        self.__num_rounds = -1
        self.__round_model_save_folder = -1
        self.__min_connected_clients_to_start = -1
        self.__project_metadata_cache_path = -1
        self.__comm_cache_folder = -1
        self.__id_number = -1

    def _initialize(self,
    server_id: int,
    num_rounds: int,
    round_model_save_folder: pathlib.PosixPath,
    min_connected_clients: int,
    initialized_model_parameters: List,
    project_metadata_cache_path: pathlib.PosixPath,
    ) -> bool:
        self.__num_rounds = num_rounds
        self.__round_model_save_folder = round_model_save_folder
        self.__min_connected_clients_to_start = min_connected_clients
        self.__id_number = server_id
        self.__project_metadata_cache_path = project_metadata_cache_path
        self.__comm_cache_folder = self.__project_metadata_cache_path.joinpath(str(self.__id_number))

        assert self.__num_rounds > 0
        assert self.__min_connected_clients_to_start >= 2

        # Refresh project cache folder
        if os.path.exists(self.__project_metadata_cache_path):
            shutil.rmtree(self.__project_metadata_cache_path)
            os.mkdir(self.__project_metadata_cache_path)
        else:
            os.mkdir(self.__project_metadata_cache_path)
        
        #------------------------- Communication protocols between clients and server initialization -------------------------#
        ## Create server-client communication cache folder
        os.mkdir(self.__comm_cache_folder)
        os.mkdir(self.__comm_cache_folder.joinpath('connect_requesting'))
        os.mkdir(self.__comm_cache_folder.joinpath('connected'))
        os.mkdir(self.__comm_cache_folder.joinpath('round_selected'))

        ## Initialize the global model parameters
        file = open(self.__comm_cache_folder.joinpath('global_model_parameters.pkl'), "wb")
        pickle.dump(initialized_model_parameters, file)
        file.close()
        #---------------------------------------------------------------------------------------------------------------------#

        # Print initialization info
        log_print('+-------------------------- Server Initialization Finished --------------------------+', 'g')
        log_print('+---> Server ID: %d' % self.__id_number, 'g')
        log_print('+---> FL iteration round: %d' % self.__num_rounds, 'g')
        log_print('+---> Min connected clients to start: %d' % self.__min_connected_clients_to_start, 'g')
        log_print('+---> Round models save folder: %s' % str(self.__round_model_save_folder), 'g')
        log_print('+------------------------------------------------------------------------------------+', 'g')
        return True

    def __connect_client(self,
        client_id: int
    ) -> bool:
        remove_message_file(self.__comm_cache_folder.joinpath('connect_requesting', str(client_id)))
        create_message_file(self.__comm_cache_folder.joinpath('connected', str(client_id)))
        return True

    def __get_request_to_connect_clients_id(self) -> List[int]:
        request_to_connect_clients_id = get_files_in_folder(self.__comm_cache_folder.joinpath('connect_requesting'))
        for i in range(len(request_to_connect_clients_id)):
            request_to_connect_clients_id[i] = int(request_to_connect_clients_id[i])
        return request_to_connect_clients_id

    def __get_connected_clients_id(self) -> List[int]:
        connect_clients_id = get_files_in_folder(self.__comm_cache_folder.joinpath('connected'))
        for i in range(len(connect_clients_id)):
            connect_clients_id[i] = int(connect_clients_id[i])
        return connect_clients_id

    def __get_round_selected_clients_id(self) -> List[int]:
        round_selected_clients_id = get_files_in_folder(self.__comm_cache_folder.joinpath('round_selected'))
        for i in range(len(round_selected_clients_id)):
            round_selected_clients_id[i] = int(round_selected_clients_id[i])
        return round_selected_clients_id

    def __aggregation_model_updates(self,
        model_updates_dictlist: List[dict],
        aggregation_weights: dict,
        layermask_dictlist: List[dict],
        para_njobs = 1
        ) -> List:
        '''Aggregate the updates of input models.
        '''
        assert len(aggregation_weights.keys()) == len(model_updates_dictlist)
        assert len(aggregation_weights.keys()) == len(layermask_dictlist)

        sum_weights = 0.
        for client_id in aggregation_weights.keys():
            sum_weights += aggregation_weights[client_id]
        for client_id in aggregation_weights.keys():
            aggregation_weights[client_id] /= sum_weights

        item = layermask_dictlist[0]
        client_id = list(item.keys())[0]
        layermask_vector = item[client_id]
        layerwise_denominator = np.zeros_like(layermask_vector, dtype = np.float32)
        for item in layermask_dictlist:
            client_id = list(item.keys())[0]
            layermask_vector = item[client_id]
            layerwise_denominator += aggregation_weights[client_id]*layermask_vector

        ## Parallelly get weighted updates of input models
        def __weight_model_updates(item: dict):
            weighted_model_updates = []
            client_id = list(item.keys())[0]
            model_updates = item[client_id]
            for layer_idx in range(len(model_updates)):
                if layerwise_denominator[layer_idx] > 0:
                    weighted_model_updates.append(model_updates[layer_idx]*aggregation_weights[client_id]/layerwise_denominator[layer_idx])
                else:
                    weighted_model_updates.append(np.zeros_like(model_updates[layer_idx]))
            return {client_id: weighted_model_updates}

        weighted_model_updates_dictlist = Parallel(n_jobs = para_njobs, prefer = "threads")(delayed(__weight_model_updates)(item) for item in model_updates_dictlist)

        ## Initialize aggregated updates
        aggregated_model_updates = []
        item = model_updates_dictlist[0]
        client_id = list(item.keys())[0]
        model_updates = item[client_id]
        for layer_idx in range(len(model_updates)):
            aggregated_model_updates.append(np.zeros_like(model_updates[layer_idx]))

        ## Parallel aggregation
        def __aggregate_weight_model_parameters(item):
            client_id = list(item.keys())[0]
            weighted_model_updates = item[client_id]
            for layer_idx in range(len(weighted_model_updates)):
                aggregated_model_updates[layer_idx] += weighted_model_updates[layer_idx]
        
        Parallel(n_jobs = para_njobs, prefer = "threads", require ='sharedmem')(delayed(__aggregate_weight_model_parameters)(item) for item in weighted_model_updates_dictlist)

        return aggregated_model_updates

    def _get_server_id(self) -> int:
        return self.__id_number

    def round_response_to_client_connection_request(self, request_to_connect_clients_id: List[int], meta_data_dictlist: List[dict]) -> List[int]:
        return request_to_connect_clients_id

    def round_selection(self, connected_clients_id: List[int], meta_data_dictlist: List[dict]) -> List[int]:
        return connected_clients_id

    def set_aggregation_model_weights(self, model_updates_dictlist: List[dict], meta_data_dictlist: List[dict]) -> dict:
        aggregate_weights = dict()
        for item in model_updates_dictlist:
            client_id = list(item.keys())[0]
            client_updates = item[client_id]
            aggregate_weights[client_id] = 0.1
        return aggregate_weights

    def __connect_clients(self, request_to_connect_clients_id: List[int]) -> bool:
        for client_id in request_to_connect_clients_id:
            self.__connect_client(client_id)
        return True

    def _start(self) -> bool:
        for r in range(self.__num_rounds):
            # Begin this round
            ## Waiting enough clients to start
            while True:
                this_round_request_to_connect_clients_id = self.__get_request_to_connect_clients_id()
                log_print("[Server Info] Round %d, %d clients request to connect" % (r, len(this_round_request_to_connect_clients_id)), color = 'g')
                meta_data_dictlist = []
                for client_id in this_round_request_to_connect_clients_id:
                    file = open(self.__comm_cache_folder.joinpath(str(client_id), 'meta_data.pkl'), "rb")
                    client_meta_data = pickle.load(file)
                    file.close()
                    meta_data_dictlist.append(client_meta_data)
                self.__connect_clients(self.round_response_to_client_connection_request(this_round_request_to_connect_clients_id, meta_data_dictlist))
                time.sleep(3)

                this_round_connected_clients_id = self.__get_connected_clients_id()
                if len(this_round_connected_clients_id) < self.__min_connected_clients_to_start:
                    log_print("[Server Info] Round %d, current %d clients connected, min %d, waiting more clients to participate..."
                                % (r, len(this_round_connected_clients_id), self.__min_connected_clients_to_start), color = 'm')
                    time.sleep(3)
                else:
                    break
            time.sleep(3)

            ## Select participate clients
            meta_data_dictlist = []
            for client_id in this_round_connected_clients_id:
                file = open(self.__comm_cache_folder.joinpath(str(client_id), 'meta_data.pkl'), "rb")
                client_meta_data = pickle.load(file)
                file.close()
                meta_data_dictlist.append(client_meta_data)

            this_round_selected_clients_id = self.round_selection(this_round_connected_clients_id, meta_data_dictlist)
            for selected_client_id in this_round_selected_clients_id:
                create_message_file(self.__comm_cache_folder.joinpath('round_selected', str(selected_client_id)))
            log_print("[Server Info] Round %d, %d/%d clients are selected to participate"
                        % (r, len(this_round_selected_clients_id), len(this_round_connected_clients_id)), 
                        color = 'g')
            time.sleep(3)

            ## Waiting for selected clients to finish local update
            while True:
                remaining_selected_clients = self.__get_round_selected_clients_id()
                log_print("[Server Info] Round %d, waiting %d/%d selected clients to finish local update..."
                            % (r, len(remaining_selected_clients), len(this_round_selected_clients_id)), color = 'm')
                time.sleep(6)
                if len(remaining_selected_clients) == 0:
                    break
            
            ## Aggregate model updates and distribute aggregated updates
            model_updates_list = []
            meta_data_dictlist = []
            layermask_dictlist = []
            for client_id in this_round_selected_clients_id:
                file = open(self.__comm_cache_folder.joinpath(str(client_id), 'local_updates.pkl'), "rb")
                client_model_updates = pickle.load(file)
                file.close()
                model_updates_list.append(client_model_updates)

                file = open(self.__comm_cache_folder.joinpath(str(client_id), 'meta_data.pkl'), "rb")
                client_meta_data = pickle.load(file)
                file.close()
                meta_data_dictlist.append(client_meta_data)

                file = open(self.__comm_cache_folder.joinpath(str(client_id), 'layermask.pkl'), "rb")
                layermask = pickle.load(file)
                file.close()
                layermask_dictlist.append(layermask)

            aggregate_weights = self.set_aggregation_model_weights(model_updates_list, meta_data_dictlist)
            aggregated_updates = self.__aggregation_model_updates(model_updates_list, aggregate_weights, layermask_dictlist, para_njobs = 4)

            file = open(self.__comm_cache_folder.joinpath('global_model_parameters.pkl'), "rb")
            last_round_global_model_parameters = pickle.load(file)
            file.close()
            updated_global_model_parameters = [last_round_global_model_parameters[layer_idx] + aggregated_updates[layer_idx] 
                                                for layer_idx in range(len(last_round_global_model_parameters))]
            
            file = open(self.__comm_cache_folder.joinpath('global_model_parameters.pkl'), "wb")
            pickle.dump(updated_global_model_parameters, file)
            file.close()
            time.sleep(3)

            ## Save the updated global model parameters
            file = open(self.__round_model_save_folder.joinpath('global_model_parameters_%d.pkl' % r), "wb")
            pickle.dump(updated_global_model_parameters, file)
            file.close()
            log_print("[Server Info] Round %d finished! " % r, 'g')
            time.sleep(3)
        
        # Training finished
        create_message_file(self.__comm_cache_folder.joinpath('exit'))
        log_print("[Server Info] Training finished!", 'b')
        return True
