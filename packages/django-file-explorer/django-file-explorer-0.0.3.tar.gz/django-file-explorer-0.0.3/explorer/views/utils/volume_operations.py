import os

from explorer.models.volume import Volume

def get_volume_location(volume_name):
    """Getting volume location using volume name."""
    # GETTING VOLUME
    volume = Volume.volumes.getIfExists(volume_name)
    if volume is None:
        return None

    # GETTING ROOT PATH
    volume_root_path = volume.getPath()
    if not os.path.exists(volume_root_path): # Volume root path does not exists.
        return None
    return volume_root_path