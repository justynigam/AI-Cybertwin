"""
Token Mapper module for Behavioral Twin.
Bi-directional mapping between raw action text tokens and integer vocabulary IDs.
"""

class TokenMapper:
    """
    Vocabulary token mapper for security action sequences.
    """

    def __init__(self, vocab_dict: dict[int, str] | None = None):
        if vocab_dict is None:
            # Default Cyber Security Action Vocabulary
            vocab_dict = {
                0: "<PAD>",
                1: "<UNK>",
                12: "LOGIN_SUCCESS",
                13: "LOGIN_FAILURE",
                45: "Access_HR_Database",
                55: "Access_Shared_Drive",
                89: "Execute_PowerShell",
                102: "Download_Large_File",
                103: "Zip_Archive_Creation",
                104: "External_FTP_Transfer",
                105: "Clear_Event_Logs",
                106: "Privilege_Escalation_Attempt",
                107: "Port_Scan_Internal_Network"
            }

        self.id_to_token: dict[int, str] = vocab_dict
        self.token_to_id: dict[str, int] = {v: k for k, v in vocab_dict.items()}

    def get_token_id(self, token_str: str) -> int:
        return self.token_to_id.get(token_str, 1)  # Fallback to <UNK>

    def get_token_str(self, token_id: int) -> str:
        return self.id_to_token.get(token_id, f"Unknown_Action_{token_id}")

    def text_sequence_to_ids(self, sequence: list[str]) -> list[int]:
        return [self.get_token_id(tok) for tok in sequence]

    def ids_to_text_sequence(self, ids: list[int]) -> list[str]:
        return [self.get_token_str(idx) for idx in ids]
