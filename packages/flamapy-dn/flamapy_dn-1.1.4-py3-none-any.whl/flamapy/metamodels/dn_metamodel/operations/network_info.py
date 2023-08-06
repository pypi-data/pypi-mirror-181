from flamapy.core.operations import Operation

from flamapy.metamodels.dn_metamodel.models import DependencyNetwork, RequirementFile, Version


class NetworkInfo(Operation):

    def __init__(self) -> None:
        self.result: dict[str, int] = {
            'direct_dependencies': 0,
            'indirect_dependencies': 0,
            'direct_cves': 0,
            'indirect_cves': 0,
            'constraints': 0
        }
        self.direct_dependencies: list[str] = []
        self.indirect_dependencies: list[str] = []
        self.direct_cves: list[str] = []
        self.indirect_cves: list[str] = []
        self.keys: list[str] = []

    def get_result(self) -> dict[str, int]:
        return self.result

    def execute(self, model: DependencyNetwork) -> None:
        for requirement_file in model.requirement_files:
            self.search(requirement_file, 'direct')
        self.result['direct_dependencies'] = len(self.direct_dependencies)
        self.result['indirect_dependencies'] = len(self.indirect_dependencies)
        self.result['direct_cves'] = len(self.direct_cves)
        self.result['indirect_cves'] = len(self.indirect_cves)

    def search(self, parent: Version | RequirementFile, level: str) -> None:
        self.result['constraints'] += len(parent.packages)
        for package in parent.packages:
            if level == 'direct':
                self.add_direct_dependencie(package.name)
            elif level == 'indirect':
                self.add_indirect_dependencie(package.name)
            key = package.name + str(package.constraints)
            if key in self.keys:
                continue
            self.keys.append(key)
            for version in package.versions:
                for cve in version.cves:
                    if level == 'direct':
                        self.add_direct_cve(cve['id'])
                    elif level == 'indirect':
                        self.add_indirect_cve(cve['id'])
                self.search(version, 'indirect')

    def add_direct_dependencie(self, dependencie_name: str) -> None:
        if dependencie_name not in self.direct_dependencies:
            self.direct_dependencies.append(dependencie_name)

    def add_indirect_dependencie(self, dependencie_name: str) -> None:
        if dependencie_name not in self.indirect_dependencies:
            self.indirect_dependencies.append(dependencie_name)

    def add_direct_cve(self, cve_id: str) -> None:
        if cve_id not in self.direct_cves:
            self.direct_cves.append(cve_id)

    def add_indirect_cve(self, cve_id: str) -> None:
        if cve_id not in self.indirect_cves:
            self.indirect_cves.append(cve_id)