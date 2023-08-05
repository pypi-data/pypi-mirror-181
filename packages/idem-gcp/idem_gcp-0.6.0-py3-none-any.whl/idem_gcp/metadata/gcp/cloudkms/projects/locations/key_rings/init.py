"""Metadata module for managing Key Rings."""


def __init__(hub):
    hub.metadata.gcp.cloudkms.projects.locations.key_rings.PATH = (
        "projects/{project}/locations/{location}/keyRings/{keyring}"
    )
