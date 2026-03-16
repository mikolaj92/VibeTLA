from __future__ import annotations

from tools.feature_spec.tla_runner import doctor_report, format_doctor_report


def main() -> int:
    report = doctor_report()
    print(format_doctor_report(report))
    return 1 if report.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
