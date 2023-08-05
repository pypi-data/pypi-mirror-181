"""Metadata module for managing Crypto Key."""


def __init__(hub):
    hub.metadata.gcp.cloudkms.projects.locations.key_rings.crypto_keys.PATH = "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{cryptokey}"
