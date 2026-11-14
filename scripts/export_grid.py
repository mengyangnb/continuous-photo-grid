"""Export a square photo collage as a continuous 3-by-3 grid."""
import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageOps


def jpeg(image, profile):
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95, subsampling=0, icc_profile=profile)
    return buffer.getvalue()


def export_grid(source, output, name):
    with Image.open(source) as original:
        profile = original.info.get("icc_profile")
        master = ImageOps.exif_transpose(original).convert("RGBA")
    width, height = master.size
    if width != height or width % 3:
        raise ValueError("母版须为边长可被 3 整除的方图")
    background = Image.new("RGBA", master.size, "#171815")
    background.alpha_composite(master)
    master = background.convert("RGB")
    tile = width // 3
    preview_tile = min(tile, 540)
    gap = max(1, round(preview_tile * 0.045))
    preview_size = 3 * preview_tile + 2 * gap
    preview = Image.new("RGB", (preview_size, preview_size), "#171815")
    destinations = {
        "master": output / f"{name}-完整拼贴.jpg",
        "preview": output / f"{name}-九宫格预览.jpg",
        "zip": output / f"{name}-朋友圈九张.zip",
    }
    for path in destinations.values():
        if path.exists():
            raise FileExistsError(f"已存在，请使用新的 --name：{path}")
    output.mkdir(parents=True, exist_ok=True)
    with ZipFile(destinations["zip"], "x") as archive:
        for index in range(9):
            row, column = divmod(index, 3)
            x, y = column * tile, row * tile
            square = master.crop((x, y, x + tile, y + tile))
            archive.writestr(f"{index + 1:02d}.jpg", jpeg(square, profile))
            thumbnail = square.resize((preview_tile, preview_tile), Image.Resampling.LANCZOS)
            step = preview_tile + gap
            preview.paste(thumbnail, (column * step, row * step))
    destinations["master"].write_bytes(jpeg(master, profile))
    destinations["preview"].write_bytes(jpeg(preview, profile))
    for path in destinations.values():
        print(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("master", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--name", default="连幅")
    args = parser.parse_args()
    if not args.name.strip() or Path(args.name).name != args.name:
        parser.error("--name 必须为单个文件名前缀")
    try:
        export_grid(args.master, args.output, args.name)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
