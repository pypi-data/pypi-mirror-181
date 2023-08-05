from typing import List, Dict, Any
import dataclasses
import json

import cq.checker
import cq.utils


SAFETY_CONNECTION_WARNING = 'warning: safety checker cannot download vulnerability database, skipping'
SAFETY_OTHER_ERROR = 'safety checker encountered an error'
SAFETY_DECODE_ERROR = 'error when decoding safety checker output'


@dataclasses.dataclass
class SafetyReportEntry:
	vulnerability_id: str
	package_name: str
	vulnerable_spec: str
	analyzed_version: str
	advisory: str


class SafetyChecker(cq.checker.Checker):
	NAME = 'safety'
	DESCRIPTION = 'Checks installed dependencies for known security vulnerabilities.'

	def run(self, modules: List[str]) -> cq.checker.CheckerResult:
		stdout, return_code = cq.utils.run_external_checker(self.NAME, ['check', '--json'])

		# 0 is returned when safety does not find a vulnerability
		# 64 is returned when safety finds a vulnerability
		# everything else should be considered as warning or error in cq
		if return_code not in (0, 64):
			if return_code == 1 and any(keyword in stdout for keyword in ('NewConnectionError', 'socket.gaierror')):
				# we never want to fail cq because of connection error of safety checker
				return_code = 0
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_CONNECTION_WARNING,
						is_error = False,
					)
				]
			else:
				# if the reason for safety checker error is not connection error, let it fail cq
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_OTHER_ERROR,
						is_error = True,
					)
				]
		else:
			try:
				data = json.loads(stdout[stdout.find('{') :])
				output = [SafetyChecker.entry_to_result_line(entry) for entry in data['vulnerabilities']]
			except (json.decoder.JSONDecodeError, TypeError):
				output = [
					cq.checker.ResultLine(
						file = None,
						line = None,
						message = SAFETY_DECODE_ERROR,
						is_error = True,
					)
				]

		return cq.checker.CheckerResult(
			checker_name = self.NAME,
			help_line = None,
			return_code = return_code,
			output = output,
		)

	@staticmethod
	def entry_to_result_line(output_entry: Dict[str, Any]) -> cq.checker.ResultLine:
		safety_report_entry = SafetyReportEntry(
			**{field.name: output_entry[field.name] for field in dataclasses.fields(SafetyReportEntry)}
		)

		return cq.checker.ResultLine(
			file = None,
			line = None,
			message = f'package: {safety_report_entry.package_name}, '
			f'affected: {safety_report_entry.vulnerable_spec}, '
			f'installed: {safety_report_entry.analyzed_version}',
			is_error = True,
		)
