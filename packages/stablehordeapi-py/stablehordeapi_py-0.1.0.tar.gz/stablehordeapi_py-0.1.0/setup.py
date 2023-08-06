# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stablehorde_api']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'msgspec>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'stablehordeapi-py',
    'version': '0.1.0',
    'description': 'Library for using Stable Horde API in Python',
    'long_description': '<h1 align="center">\nStableHordeAPI.py\n</h1>\n<h2 align="center">Simple wrapper around Stable Horde API</h2>\n\n# Content\n- [Installation](#installation)\n- [Usage](#usage)\n- [Examples](#examples)\n- [License](#license)\n\n# Installation\n```\npip install stablehordeapi.py\n```\n\n# Usage\n```python\nimport asyncio\n\nfrom stablehorde_api import StableHordeAPI\n\nasync def main():\n    client = StableHordeAPI("Your Stable Horde token here")\n    await client.generate_from_txt(\n        "Futuristic cyberpunk landscape, 8k, hyper realistic, cinematic"\n    )\n\nasyncio.run(main())\n```\nThis code will generate an image based on your prompt and save it as "{unix timestamp}\\_0.webp" in your current directory.\n\nAdditionally, you can specify file name:\n```python\nawait client.generate_from_txt(\n    "Your prompt...",\n    filename="my_image"\n)\n```\nIn that case, your file will be saved as "my\\_image.webp"\n\nHowever, you\'ll probably want more control over how image is generated. So, for example, you can do this:\n```python\nimport asyncio\nfrom stablehorde_api import GenerationInput, ModelGenerationInputStable\n\nasync def main():\n    client = StableHordeAPI("Your Stable Horde token here")\n    payload = GenerationInput(\n        "masterpiece, best quality, ((Hu Tao)), brown hair, long hair, flower-shaped pupils",\n\tparams=ModelGenerationInputStable(\n\t    height=512,\n\t    width=768,\n\t    steps=50,\n\t    post_processing=[\'RealESRGAN_x4plus\']\n\t),\n\tnsfw=True,\n\tcensor_nsfw=False,\n\tmodels=[\'Anything Diffusion\'],\n\tn=5\n    )\n    # payload can also be a dict, which is useful, if something new added\n    txt2img_rsp = await client.txt2img_request(payload)\n    img_uuid = txt2img_rsp.id\n\n    done = False\n    while not done:\n        # Checking every second if image is generated\n        await asyncio.sleep(1)\n        generate_check = await client.generate_check(img_uuid)\n\tif generate_check.done == 1:\n\t    done = True\n\n    # Generating a status which has all generations (in our case,\n    # there should be 5 generations, because n is set to 5)\n    generate_status = await client.generate_status(img_uuid)\n    generations = generate_status.generations\n```\nAfter that, all generations will be in `generations` variable. To access first image, use `generations[0].img`\n\n# Examples\nThis example will generate 3 Hu Tao images using Anything Diffusion model.\n```python\nimport asyncio\nimport base64\n\nimport aiofiles\nfrom stablehorde_api import GenerationInput, ModelGenerationInputStable\n\nasync def main():\n    client = StableHordeAPI("Your Stable Horde token here")\n    payload = GenerationInput(\n        "masterpiece, best quality, ((Hu Tao)), brown hair, long hair, flower-shaped pupils",\n\tmodels=[\'Anything Diffusion\'],\n\tn=3\n    )\n    txt2img_rsp = await client.txt2img_request(payload)\n    img_uuid = txt2img_rsp.id\n\n    done = False\n    while not done:\n        await asyncio.sleep(1)\n        generate_check = await client.generate_check(img_uuid)\n\tif generate_check.done == 1:\n\t    done = True\n\n    generate_status = await client.generate_status(img_uuid)\n    generations = generate_status.generations\n    for num, generation in enumerate(generations):\n        new_filename = f\'{filename}_{num}.webp\'\n        async with aiofiles.open(new_filename, \'wb\') as file:\n            b64_bytes = generation.img.encode(\'utf-8\')\n            img_bytes = base64.b64decode(b64_bytes)\n            awat file.write(img_bytes)\n```\nIf you set `r2` to true, then you will need to request content from the link in generations. You can do that by using aiohttp:\n```python\nimport aiohttp\n...\n\naiohttp_client = aiohttp.ClientSession()\n...\n\nimg_rsp = (await aiohttp_client.request(url=generation.img)).content\nimg_bytes = await img_rsp.read()\n```\n\n# License\n[MIT License](./LICENSE)\n\n',
    'author': 'Timur Bogdanov',
    'author_email': 'timurbogdanov2008@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/timius100/StableHordeAPI.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
