"""PowerPoint slide image rendering support."""

from pathlib import Path

import win32com.client
def render_presentation(source_path, output_folder):
    """Export PowerPoint slides as PNG images."""

    source = Path(source_path).resolve()
    output = Path(output_folder).resolve()

    if not source.is_file():
        raise FileNotFoundError(
            f"PowerPoint presentation not found: {source}"
        )

    if source.suffix.lower() != ".pptx":
        raise ValueError("Only .pptx presentations are supported.")

    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise FileExistsError(
            "The preview folder is not empty. "
            "Existing files have been left unchanged."
        )

    powerpoint = None
    presentation = None

    try:
        powerpoint = win32com.client.DispatchEx(
            "PowerPoint.Application"
        )

        presentation = powerpoint.Presentations.Open(
            str(source),
            True,   # ReadOnly
            False,  # Untitled
            False,  # WithWindow
        )

        slide_count = presentation.Slides.Count

        for number in range(1, slide_count + 1):
            image_path = output / f"slide_{number:03d}.png"

            presentation.Slides(number).Export(
                str(image_path),
                "PNG",
                1280,
                720,
            )

        return slide_count

    finally:
        if presentation is not None:
            presentation.Close()

        if powerpoint is not None:
            powerpoint.Quit()