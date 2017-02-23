import os.path
import setuptools

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

# Get test requirements
test_requirements = []
with open(os.path.join(LOCAL_DIR, 'requirements-test.txt'), 'r') as infile:
    for line in infile:
        line = line.strip()
        if line and not line[0] == '#':  # ignore comments
            test_requirements.append(line)

setuptools.setup(
    name='pencroft',
    version='0.3',
    license='BSD',
    packages=setuptools.find_packages(),
    extras_require={'test': test_requirements},
    include_package_data=True,
    zip_safe=False,
)
