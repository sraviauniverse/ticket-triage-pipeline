import sys
import yaml


def update_image_tag(manifest_path, new_tag):
    with open(manifest_path) as handle:
        manifest = yaml.safe_load(handle)

    container = manifest["spec"]["predictor"]["containers"][0]
    image_name = container["image"].split(":")[0]
    container["image"] = f"{image_name}:{new_tag}"

    with open(manifest_path, "w") as handle:
        yaml.safe_dump(manifest, handle, default_flow_style=False, sort_keys=False)

    return container["image"]


if __name__ == "__main__":
    manifest_path, new_tag = sys.argv[1], sys.argv[2]
    updated_image = update_image_tag(manifest_path, new_tag)
    print(f"Manifest now references: {updated_image}")
