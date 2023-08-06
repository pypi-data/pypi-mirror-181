from requests import get

from .exceptions import *
from .settings import API_URL

__all__ = ["NonlocalBox"]


class NonlocalBox:
    """
    An API for simulating nonlocal no-signalling correlations.

    Attributes
    ----------
    api_key : str
        The API key to use the service.
    box_id : int
        The ID of the box use for the simulation(s).
    box_type_id : int
        The ID of the type of the box.
    role : str
        The role in the simulation. Can be Alice of Bob

    Raises
    ------
    TypeError
        If *api_key* is not a string.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.box_id = None
        self.box_type_id = None
        self.role = None
        if not isinstance(self.api_key, str):
            raise TypeError("api_key must be a string")

    def invite(self, partner, box_type_id, box_name):
        """
        Invite *partner* for the game, set `self.box_id` to the returned box_id
        and set the type of *box_id* to `self.box_type_id`.

        Parameters
        ----------
        partner : str
            The username of the partner to play with
        box_type_id : int
            The ID of the box to use in the game
        box_name : str
            A user defined name of the box

        Returns
        -------
        box_id : int
            The ID of the newly created box named *box_name*.

        Raises
        ------
        `~nonlocalbox.exception.StatusError`
            If a nonzero status value returned by the server.
        """
        r = get(API_URL + "/invitePartner",
                params={
                    "apiKey": self.api_key,
                    "inviteUserName": partner,
                    "boxTypeID": box_type_id,
                    "boxName": box_name,
                })
        _check_status(r)
        self.box_id = r.json()["boxID"]
        self.box_type_id = box_type_id
        return self.box_id

    def initialize(self, box_id, i_want_to_be_bob=False):
        """
        Set *box_id* without verification and set `self.role` to Alice
        if it is in the list of boxes; set it to Bob otherwise.

        Parameters
        ----------
        box_id : int
            The ID of the box used in the game.
        i_want_to_be_bob : bool, optional
            If aliceUser and bobUser is the same in the box with box ID *box_id*
            this boolean will tell the server that the user wants to be in the role Bob.
        """
        self.box_id = box_id
        box = next((i for i in self.list_boxes() if i["id"] == str(box_id)), None)
        if box is None:
            self.role = "Bob"
        elif box["aliceUser"] == box["bobUser"]:
            self.role = "Bob" if i_want_to_be_bob else "Alice"
        else:
            self.role = "Alice"

    def use(self, input, transaction_id):
        """Use box with *input* and *transaction_id*.

        Parameters
        ----------
        input : int
            The input of the box.
        transaction_id : str
            The transaction ID of the game.

        Returns
        -------
        res : int
            The output of the box.

        Raises
        ------
        `~nonlocalbox.exceptions.StatusError`
            If a nonzero status value returned by the server.
        `~nonlocalbox.exceptions.UnknownBoxTypeError`
            If box_id does not exist in the database.
        """
        if self.box_id is None:
            raise UninitializedBoxError(f"No box initialized.")
        r = get(API_URL + "/useBox",
                params={
                    "apiKey": self.api_key,
                    "boxID": self.box_id,
                    "transactionID": transaction_id,
                    "x" if self.role == "Alice" else "y": input,
                })
        _check_status(r)
        return r.json()["a"] if self.role == "Alice" else r.json()["b"]

    def list_box_types(self):
        """
        List all available box types.

        Returns
        -------
        r : list
            A list of box types

        Raises
        ------
        `~nonlocalbox.exceptions.StatusError`
            If the server returns a nonzero status.
        """
        r = get(API_URL + "/listBoxTypes",
                params={"apiKey": self.api_key})
        _check_status(r)
        return r.json()["boxTypes"]

    def list_boxes(self):
        """
        List all boxes where the user has role 'Alice'.

        Returns
        -------
        boxes : list
            A list of boxes where the user has role 'Alice'.

        Raises
        ------
        `~nonlocalbox.exceptions.StatusError`
            If a nonzero status value returned by the server.
        """
        r = get(API_URL + "/listBoxes",
                params={"apiKey": self.api_key})
        _check_status(r)
        return r.json()["boxes"]

    def box_type_info(self):
        """
        Return some information on box type stored in ``self``.

        Returns
        -------
        info : dict
            All information available on box type.

        Raises
        ------
        `~nonlocalbox.exceptions.StatusError`
            If a nonzero status value returned by the server.
        """
        r = get(API_URL + "/boxTypeInfo",
                params={
                    "apiKey": self.api_key,
                    "boxTypeID": self.box_type_id,
                })
        _check_status(r)
        return r.json()["boxTypes"]


def _check_status(resp):
    if resp.status_code != 200:
        raise ServiceError(f"Received an invalid status code from the server: {resp.status_code}.")
    if resp.json()["status"] != 0:
        raise StatusError(f"Nonzero status returned: {resp.json()['status']}")