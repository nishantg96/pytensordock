import json
import requests
from typing import Optional, Dict, Any


class TensorDockWrapper:
    def __init__(self, api_key: str, api_token: str, debug: bool = False):
        """Initialize the TensorDockAPIWrapper.

        Args:
            api_key (str): The API key for authentication.
            api_token (str): The API token for authentication.
        """
        self.base_url = "https://marketplace.tensordock.com/api/v0/"
        self.api_key = api_key
        self.api_token = api_token
        self.debug = debug

    def _send_request(
        self, method: str, endpoint: str, payload: Optional[dict] = None, params: Optional[dict] = None
    ) -> Dict[str, Any]:
        """Send a request to the TensorDock API.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint.
            payload (Optional[dict]): The request payload.
            params (Optional[dict]): The request parameters.

        Returns:
            dict: The JSON response.
        """
        url = self.base_url + endpoint
        response = requests.request(method, url, data=payload, params=params)

        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    def _parse_response(self, response: dict) -> Dict[str, Any]:
        """Parse and pretty-print the JSON response.

        Args:
            response (dict): The JSON response.
        """
        try:
            json_formatted_str = json.dumps(response, indent=2)
            print(json_formatted_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def stop_server(self, server_uuid: str, disassociate_resources: bool = True) -> Dict[str, Any]:
        """
        Create a request to stop a server on an authorization. If the server is stopped without releasing the GPU, it will be billed at the same rate as a running server. If the GPU is released, it will only be billed for the storage costs.

        Args:
            server_uuid (str): The UUID of the server to stop.
            disassociate_resources (bool): Optional - set to "True" if you want to release the GPU when stopping the VM.
            
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/stop/single"
        payload = {
            "api_key": self.api_key,
            "api_token": self.api_token,
            "server": server_uuid,
            "disassociate_resources": str(disassociate_resources).lower(),
        }
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def start_server(self, vm_uuid: str) -> Dict[str, Any]:
        """
        Create a request to start a server on an authorization.

        Args:
            vm_uuid (str): The UUID of the virtual machine to start.
            
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/start/single"
        payload = {"api_key": self.api_key, "api_token": self.api_token, "server": vm_uuid}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def modify_server(
        self, server_uuid: str, gpu_model: str, gpu_count: int, ram: int, vcpus: int, storage: int
    ) -> Dict[str, Any]:
        """
        Modify the specifications of a virtual machine. Your virtual machine must be of type "network storage" and stopped before modifying.

        Args:
            server_uuid (str): The UUID of the virtual machine to modify.
            gpu_model (str): You can get available GPU models on a hostnode from the hostnodes list API endpoint. Examples: geforcertx3090-pcie-24gb, rtxa6000-pcie-48gb, etc.
            gpu_count (int): Number of GPUs.
            ram (int): RAM amount.
            vcpus (int): Number of vCPUs.
            storage (int): Storage amount.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/modify/single"
        payload = {
            "api_key": self.api_key,
            "api_token": self.api_token,
            "server_id": server_uuid,
            "gpu_model": gpu_model,
            "gpu_count": str(gpu_count),
            "ram": str(ram),
            "vcpus": str(vcpus),
            "storage": str(storage),
        }
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def delete_server(self, server_uuid: str) -> Dict[str, Any]:
        """
        Create a request to delete a server.

        Args:
            server_uuid (str): The UUID of the virtual machine to delete.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/delete/single"
        payload = {"api_key": self.api_key, "api_token": self.api_token, "server": server_uuid}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def list_virtual_machines(self) -> Dict[str, Any]:
        """
        List all current virtual machines registered under an organization.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/list"
        payload = {"api_key": self.api_key, "api_token": self.api_token}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def get_vm_details(self, server_uuid: str) -> Dict[str, Any]:
        """
        Retrieve the details of a specific virtual machine.

        Args:
            server_uuid (str): The UUID of the virtual machine to retrieve details.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/get/single"
        payload = {"api_key": self.api_key, "api_token": self.api_token, "server": server_uuid}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def soft_validate_new_spot_instance(
        self, gpu_count: int, gpu_model: str, vcpus: int, hostnode: str, ram: int, storage: int, price: float
    ) -> Dict[str, Any]:
        """
        To validate if an interruptible instance of a given price will succeed, you can send this request.

        If the "success" field is false, then you must bid higher and confirm that enough resources are available. If the "success" field is true, then a deployment of the resources you selected will succeed.

        Args:
            gpu_count (int): Number of GPUs.
            gpu_model (str): GPU model.
            vcpus (int): Number of vCPUs.
            hostnode (str): Hostnode ID.
            ram (int): RAM amount.
            storage (int): Storage amount.
            price (float): Bid price for the spot instance.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/spot/validate/new"
        payload = {
            "gpu_count": str(gpu_count),
            "gpu_model": gpu_model,
            "vcpus": str(vcpus),
            "hostnode": hostnode,
            "ram": str(ram),
            "storage": str(storage),
            "price": str(price),
            "api_key": self.api_key,
            "api_token": self.api_token,
        }
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def soft_validate_existing_spot_instance(self, server: str, price: float) -> Dict[str, Any]:
        """
        To validate if an existing VM, modified to this price, will succeed, you can send this request.

        If the "success" field is false, then you must bid higher and confirm that enough resources are available. If the "success" field is true, then your VM will start with the new price (or your VM will continue to run at the new price).

        Args:
            server (str): The UUID of the virtual machine to validate.
            price (float): Bid price for the spot instance.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/spot/validate/new"
        payload = {
            "server": server,
            "price": str(price),
            "api_key": self.api_key,
            "api_token": self.api_token,
        }
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def deploy_machine(
        self,
        name: str,
        gpu_count: int,
        gpu_model: str,
        vcpus: int,
        ram: int,
        external_ports: list,
        internal_ports: list,
        hostnode: str,
        storage: int,
        operating_system: str,
        password: str,
        deployment_type: str = "local",
        cpu_model: str = None,
        location: str = None,
        cloudinit_script: str = None,
        price_type: str = None,
        price: float = None,
    ) -> Dict[str, Any]:
        """
        This endpoint allows a single deployment of a machine, based on parameters you control. Pass in, via the REST body, the following variables., as shown with some examples

        Ports should be sent as a list structed with curly braces with commas and spaces as separators of the ports themselves. The first index of the externally requested port will forward into the first index of the internally requested port, and so on... You can view available ports for each machine through the hostnodes list API.

        Args:
            name (str): Name of your VM to be displayed in the dashboard
            gpu_count (int): Number of GPUs.
            gpu_model (str): You can get available GPU models on a hostnode from the hostnodes list API endpoint. Examples: geforcertx3090-pcie-24gb, rtxa6000-pcie-48gb, etc.
            vcpus (int): Number of vCPUs.
            ram (int): RAM amount.
            external_ports (list): External port mappings.
            internal_ports (list): Internal port mappings.
            hostnode (str): Hostnode ID.
            storage (int): Storage amount.
            operating_system (str): Operating system.
            password (str): Password for the virtual machine.
            deployment_type (str): Optional field to specify either a "network" or "local" deployment. For CPU-only deployments, use "network". Defaults to "local".
            cpu_model (str): Required if deploying a CPU-only server.
            location (str): Required if deployment type is "network". Can be either "New York City, New York, United States", "Chicago, Illinois, United States", or "Las Vegas, Nevada, United States".
            cloudinit_script (str): String of text to append to our cloud-init script, with newlines substituted for \n.
            price_type (str): Optional field to deploy a spot instance.
            price (float): Optional field to set bid amount for spot deployment.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/deploy/single"
        payload = {
            "api_key": self.api_key,
            "api_token": self.api_token,
            "name": name,
            "gpu_count": str(gpu_count),
            "gpu_model": gpu_model,
            "vcpus": str(vcpus),
            "ram": str(ram),
            "external_ports": "{" + ", ".join(map(str, external_ports)) + "}",
            "internal_ports": "{" + ", ".join(map(str, internal_ports)) + "}",
            "hostnode": hostnode,
            "storage": str(storage),
            "operating_system": operating_system,
            "password": password,
            "deployment_type": deployment_type,
            "cpu_model": cpu_model,
            "location": location,
            "cloudinit_script": cloudinit_script,
            "price_type": price_type,
            "price": str(price),
        }
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def list_available_hostnodes(
        self,
        min_vcpus: Optional[int] = None,
        min_ram: Optional[int] = None,
        min_storage: Optional[int] = None,
        min_vram: Optional[int] = None,
        min_gpu_count: Optional[int] = None,
        requires_rtx: Optional[bool] = None,
        requires_gtx: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        This gets a list of all available hostnodes and stock for GPUs. These hostnodes are categorized as "local storage". "Network storage" GPUs can be provisioned by following the instructions listed under the deployment endpoint. You will need to keep track of the GPU model and available CPU/RAM for the deployment step. All params are optional, but can be added to filter for certain hostnodes.

        Note: If you include your organization's API key and token in the request, like such:

        https://marketplace.tensordock.com/api/v0/client/deploy/hostnodes?api_key=KEY&api_token=TOKEN

        Hostnodes that are reserved for your organization will also show up in the list.

        Args:
            min_vcpus (int): Minimum number of vCPUs.
            min_ram (int): Minimum amount of RAM.
            min_storage (int): Minimum SSD storage amount in GB.
            min_vram (int): Minimum VRAM amount.
            min_gpu_count (int): Minimum number of GPUs.
            requires_rtx (bool): Requires RTX GPU.
            requires_gtx (bool): Requires GTX GPU.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "client/deploy/hostnodes"
        params = {
            "api_key": self.api_key,
            "api_token": self.api_token,
            "minvCPUs": min_vcpus,
            "minRAM": min_ram,
            "minStorage": min_storage,
            "minVRAM": min_vram,
            "minGPUCount": min_gpu_count,
            "requiresRTX": requires_rtx,
            "requiresGTX": requires_gtx,
        }
        response = self._parse_response(self._send_request("GET", endpoint, params=params))
        if self.debug:
            self._parse_response(response)
        return response

    def list_authorizations(self) -> Dict[str, Any]:
        """Get a list of all authorizations."""
        endpoint = "auth/list"
        payload = {"api_key": self.api_key, "api_token": self.api_token}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def retrieve_balance(self) -> Dict[str, Any]:
        """
        Through this endpoint, you can easily retrieve your current balance and spending rate to monitor your balance.

        Remember, once your balance runs out, your servers are automatically deleted — so please constantly monitor and understand your billing situation to ensure that this does not occur.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "billing/balance"
        payload = {"api_key": self.api_key, "api_token": self.api_token}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def test_authorization(self) -> Dict[str, Any]:
        """
        Here you can test that an authorization is registered and working.

        Simply pass in your API key as api_key and API token as api_token, and confirm that we return true!

        We will return an object {"success": true} if your authorization key and token are valid.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = "auth/test"
        payload = {"api_key": self.api_key, "api_token": self.api_token}
        response = self._send_request("POST", endpoint, payload)
        if self.debug:
            self._parse_response(response)
        return response

    def get_specific_hostnode(self, id: str) -> Dict[str, Any]:
        """Instead of returning all available hostnodes, you can also return the information of a specific one based on its UUID.

        Args:
            id (str): The ID of the hostnode.
        
        Returns:
            dict: The JSON response.
        """
        endpoint = f"client/deploy/hostnodes/{id}"
        response = self._parse_response(self._send_request("GET", endpoint))
        if self.debug:
            self._parse_response(response)
        return response


if __name__ == "__main__":
    """
    Create an API key/token
    Authentication is done organization-wide: API keys and tokens are tied to an organization and not a specific user (unlike our Core Cloud product). Thus, deleting a user from an organization will not remove any API keys.

    You can also create an unlimited number of authorization pairs for maximum granularity. We recommend one authorization for each external integration you make for best security.

    You can get access to your API token and info here: https://marketplace.tensordock.com/api
    """
    
    api_key = "API_KEY"
    api_token = "API_TOKEN"

    wrapper = TensorDockWrapper(api_key=api_key, api_token=api_token, debug=True)
    wrapper.test_authorization()