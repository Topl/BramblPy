import pytest

NEW_KEYFILE = {
    'json': {
        'Crypto': {
            'cipher': 'aes-256-ctr',
            'cipherparams': {
                'iv': 'D1bnzq5VUH3R6TPvkrqCnq',
            },
            'ciphertext': 'ErMJrbu35u8Y6NbuagEaZKWkUPk9MoFD4dfxeQzvPXL4',
            'kdf': 'scrypt',
            'kdfparams': {
                'dklen': 32,
                'n': 8192,
                'p': 1,
                'r': 8,
                'salt': '2G3JuACUCnjLFcCmDmD9pSUWY9ryRpwVj89bioAFbUjt',
            },
            'mac': '3ibMYUndvubiUnb2nnisiRxZCWW5xcgqFCE97WUu5KFv',
        },
        'address': 'AUEgyX7QfKW2x2RVthNheLPAToQwxYjYiACgLjRY5XKPW5pMRG72',
        'id': '3c8efdd6-d538-47ec-b241-36783d3418b9',
        'version': 2,
    },
    'password': 'test',
    'priv': '4vJ9JU1bJJE96FWSJKvHsmmFADCg4gpZQff4P3bkLKi',
}


@pytest.fixture()
def keyfile_data():
    return NEW_KEYFILE
