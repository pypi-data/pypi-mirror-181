from typing import List, Set
import os.path
import re

import bellybutton.cli
import bellybutton.parsing

import cq.checker
import cq.utils


class BellybuttonChecker(cq.checker.Checker):
	NAME = 'bellybutton'
	DESCRIPTION = 'Launch Bellybutton linter on given modules.'
	HELP_LINE = 'use `# bb: ignore` for disabling bellybutton on particular line'
	PYTEST_INI_FILE = 'pytest.ini'
	ASYNCIO_MODE_AUTO_REGEX = r'asyncio_mode\s+=\s+auto'
	ASYNCIO_MODE_RULE_NAME = 'MissingPytestMarkAsyncio'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		files: Set[str] = set()

		for file in cq.utils.get_all_python_files(modules):
			files.add(file)

		bellybutton_conf = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.bellybutton.yml')
		with open(bellybutton_conf, 'r', encoding = 'utf-8') as f:
			rules = bellybutton.parsing.load_config(f)

		rules = self._filter_rules(rules)

		results = bellybutton.cli.linting_failures(files, rules)

		output: List[cq.checker.ResultLine] = []
		for result in results:
			output.append(
				cq.checker.ResultLine(
					file = result.path,
					line = result.lineno,
					message = result.rule.description,
					is_error = True,
				)
			)

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = self.HELP_LINE,
			return_code = 0 if not output else 1,
			output = output,
		)

	def _filter_rules(self, rules: List[bellybutton.parsing.Rule]) -> List[bellybutton.parsing.Rule]:
		project_root = cq.utils.get_project_root_dir()
		# if we have set asyncio_mode = auto in pytest.ini we should remove rule MissingPytestMarkAsyncio
		# see https://github.com/pytest-dev/pytest-asyncio#auto-mode
		if project_root is not None and os.path.exists(os.path.join(project_root, self.PYTEST_INI_FILE)):
			with open(os.path.join(project_root, self.PYTEST_INI_FILE), encoding = 'utf-8') as f:
				if re.search(self.ASYNCIO_MODE_AUTO_REGEX, f.read()):
					rules = [rule for rule in rules if rule.name != self.ASYNCIO_MODE_RULE_NAME]
		return rules
