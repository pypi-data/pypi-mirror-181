# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['k8smap']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.12.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'flake8>=6.0.0,<7.0.0',
 'mypy>=0.991,<0.992',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['k8smap = k8smap.main:cli']}

setup_kwargs = {
    'name': 'k8smap',
    'version': '0.1.1',
    'description': '',
    'long_description': '# k8smap\n\nk8smap is a tool to generate a diagram a diagram text file from kubernetes resource descriptions. \nI implemented this to get a faster understanding of the resources in a given helm chart.\nAlso it helps me document the infrastructure automatically visually for my colleagues.\n\n# Quick start\n\n```\npoetry add k8smap\n\nk8smap -i filename.yaml\n```\n\n# Example\nYou can clone the repo and test it locally.\n\n```\nhelm template example > example.yaml \npoetry run k8smap -i infratest.yaml\n```\n\nThis will generate the following output to file file `output.d2`:\n```\nService_pawn:pawn {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/svc.svg\n  shape: image\n}\nService_bishop:bishop {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/svc.svg\n  shape: image\n}\nPod_bishop-nginx:bishop-nginx {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/pod.svg\n  shape: image\n}\nDeployment_nginx-deployment:nginx-deployment {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/deploy.svg\n  shape: image\n}\nPod_nginx-deployment:nginx-deployment {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/pod.svg\n  shape: image\n}\nIngress_pawn-ingress:pawn-ingress {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/ing.svg\n  shape: image\n}\nIngress_bishop-ingress:bishop-ingress {\n  icon: https://raw.githubusercontent.com/kubernetes/community/master/icons/svg/resources/labeled/ing.svg\n  shape: image\n}\nService_pawn --> Pod_nginx-deployment\nService_bishop --> Pod_bishop-nginx\nDeployment_nginx-deployment --> Pod_nginx-deployment\nIngress_pawn-ingress --> Service_pawn\nIngress_bishop-ingress --> Service_bishop\n```\n\nTo generate an image for this graph you can run d2.\n```\nd2 output.d2 out.svg\n```\n\n![Visualization of the helm chart](./docs/example-diagram.png)\n\nOr generate a mermaid flowchart.\n```\nmapk8s -i filename.yaml -f mermaid\n```\n\n# Components\n\nSo far the following components are implemented:\n\n- [x] Pod\n- [x] Deployment\n- [x] Ingress\n- [x] Service\n- [x] Config Map\n- [ ] Service Account\n- [ ] Network Policy\n- [ ] Cron Job\n- [ ] Job\n- [ ] Secret\n- [ ] Volume\n- [ ] Persistent Volume\n- [ ] Persistent Volume Claim\n\n# Output formats\nSo far the following output languages are supported:\n- [x] [D2](https://d2lang.com/tour/intro/)\n- [x] [Mermaid](https://mermaid-js.github.io/mermaid/#/)\n\nUse the `-f [d2, mermaid]` flag to specify the format.\n\n# License\nThis is unclear right now and needs to be checked. \nAs I am using in this code svg from Kubernetes, I first have to evaluate what license I can use.\n',
    'author': 'Paul Beck',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
