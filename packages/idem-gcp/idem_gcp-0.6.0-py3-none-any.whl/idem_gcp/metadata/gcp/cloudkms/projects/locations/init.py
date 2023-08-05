"""Metadata module for managing Locations."""


def __init__(hub):
    hub.metadata.gcp.cloudkms.projects.locations.PATH = (
        "projects/{project}/locations/{location}"
    )
