import azure.functions as func
from rio_tiler.io import COGReader
from rio_tiler.utils import render
from PIL import Image
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    container = req.route_params.get('container')
    filename = req.route_params.get('filename')
    z = int(req.route_params.get('z'))
    x = int(req.route_params.get('x'))
    y = int(req.route_params.get('y'))

    cog_path = f"https://{container}.blob.core.windows.net/{filename}"

    try:
        with COGReader(cog_path) as cog:
            tile, mask = cog.tile(x, y, z)
            img = render(tile, mask=mask)

            # Converte o tile renderizado para bytes
            bytes_io = io.BytesIO()
            img.save(bytes_io, format='JPEG')
            bytes_io.seek(0)

            return func.HttpResponse(bytes_io.read(), mimetype="image/jpeg")
    except Exception as e:
        return func.HttpResponse(f"Error processing tile: {str(e)}", status_code=500)