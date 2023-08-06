import json
from collections import namedtuple
from copy import deepcopy

import pytest
from pytest_voluptuous import Partial, S
from voluptuous import Optional, validators

from ggshield.core.utils import Filemode
from ggshield.output import JSONOutputHandler, OutputHandler
from ggshield.output.json.schemas import JSONScanCollectionSchema
from ggshield.scan import (
    Commit,
    Result,
    Results,
    ScanCollection,
    ScanContext,
    ScanMode,
    SecretScanner,
)
from ggshield.scan.scannable import File
from tests.unit.conftest import (
    _MULTIPLE_SECRETS_PATCH,
    _NO_SECRET_PATCH,
    _ONE_LINE_AND_MULTILINE_PATCH,
    _ONE_LINE_AND_MULTILINE_PATCH_CONTENT,
    _SINGLE_ADD_PATCH,
    _SINGLE_DELETE_PATCH,
    _SINGLE_MOVE_PATCH,
    TWO_POLICY_BREAKS,
    UNCHECKED_SECRET_PATCH,
    VALID_SECRET_PATCH,
    my_vcr,
)


ExpectedScan = namedtuple("expectedScan", "exit_code matches first_match want")

_EXPECT_NO_SECRET = {
    "content": "@@ -0,0 +1 @@\n+this is a patch without secret\n",
    "filename": "test.txt",
    "filemode": Filemode.NEW,
}

SCHEMA_WITHOUT_INCIDENTS = S(
    Partial(
        {
            "id": "path",
            "total_incidents": int,
            "total_occurrences": int,
            "type": "test",
        }
    )
)


SCHEMA_WITH_INCIDENTS = S(
    Partial(
        {
            "secrets_engine_version": validators.Match(r"\d\.\d{1,3}\.\d"),
            "results": validators.All(
                [
                    {
                        "filename": str,
                        "mode": validators.Any(
                            "MODIFY",
                            "RENAME",
                            "NEW",
                            "DELETE",
                            "PERMISSION_CHANGE",
                        ),
                        "total_incidents": validators.All(int, min=1),
                        "total_occurrences": validators.All(int, min=1),
                        Optional("validity"): validators.Any(
                            "valid",
                            "failed_to_check",
                            "invalid",
                            "not_checked",
                            "no_checker",
                        ),
                        "incidents": validators.All(
                            [
                                {
                                    "break_type": str,
                                    "policy": str,
                                    "total_occurrences": validators.All(int, min=1),
                                }
                            ],
                            validators.Length(min=1),
                        ),
                    }
                ],
                validators.Length(min=1),
            ),
        }
    )
)


@pytest.mark.parametrize(
    "name,input_patch,expected_exit_code",
    [
        ("multiple_secrets", _MULTIPLE_SECRETS_PATCH, 1),
        ("simple_secret", UNCHECKED_SECRET_PATCH, 1),
        ("test_scan_file_secret_with_validity", VALID_SECRET_PATCH, 1),
        ("one_line_and_multiline_patch", _ONE_LINE_AND_MULTILINE_PATCH, 1),
        ("no_secret", _NO_SECRET_PATCH, 0),
        ("single_add", _SINGLE_ADD_PATCH, 1),
        ("single_delete", _SINGLE_DELETE_PATCH, 1),
        ("single_move", _SINGLE_MOVE_PATCH, 1),
    ],
    ids=[
        "_MULTIPLE_SECRETS",
        "_SIMPLE_SECRET",
        "_SIMPLE_SECRET-validity",
        "_ONE_LINE_AND_MULTILINE_PATCH",
        "_NO_SECRET",
        "_SINGLE_ADD_PATCH",
        "_SINGLE_DELETE_PATCH",
        "_SINGLE_MOVE_PATCH",
    ],
)
def test_json_output(client, cache, name, input_patch, expected_exit_code):
    c = Commit()
    c._patch = input_patch
    handler = JSONOutputHandler(verbose=True, show_secrets=False)

    with my_vcr.use_cassette(name):
        scanner = SecretScanner(
            client=client,
            cache=cache,
            scan_context=ScanContext(
                scan_mode=ScanMode.PATH,
                command_path="external",
            ),
        )
        results = scanner.scan(c.files)

        scan = ScanCollection(id="path", type="test", results=results)
        json_flat_results = handler._process_scan_impl(scan)
        exit_code = OutputHandler._get_exit_code(scan)

        assert exit_code == expected_exit_code
        assert SCHEMA_WITHOUT_INCIDENTS == JSONScanCollectionSchema().loads(
            json_flat_results
        )
        if expected_exit_code:
            assert SCHEMA_WITH_INCIDENTS == JSONScanCollectionSchema().loads(
                json_flat_results
            )


@pytest.mark.parametrize("verbose", [True, False])
@pytest.mark.parametrize("ignore_known_secrets", [True, False])
@pytest.mark.parametrize(
    "secrets_types", ["only_new_secrets", "only_known_secrets", "mixed_secrets"]
)
def test_ignore_known_secrets(verbose, ignore_known_secrets, secrets_types):
    """
    GIVEN policy breaks
    WHEN generating json output
    THEN if ignore_known_secrets is used, include "known_secret" field for the known policy breaks in the json output
    """
    output_handler = JSONOutputHandler(show_secrets=True, verbose=verbose)

    result: Result = Result(
        File(
            document=_ONE_LINE_AND_MULTILINE_PATCH_CONTENT,
            filename="leak.txt",
            filemode=Filemode.NEW,
        ),
        scan=deepcopy(TWO_POLICY_BREAKS),  # 2 policy breaks
    )

    all_policy_breaks = result.scan.policy_breaks

    known_policy_breaks = []
    new_policy_breaks = all_policy_breaks

    # add known_secret for the secrets that are known, when the option is, the known_secret field is not returned
    if ignore_known_secrets:
        if secrets_types == "only_known_secrets":
            known_policy_breaks = all_policy_breaks
            new_policy_breaks = []
        elif secrets_types == "mixed_secrets":
            # set only first policy break as known
            known_policy_breaks = all_policy_breaks[:1]
            new_policy_breaks = all_policy_breaks[1:]

    for policy_break in known_policy_breaks:
        policy_break.known_secret = True

    # call output handler
    output = output_handler._process_scan_impl(
        ScanCollection(
            id="outer_scan",
            type="outer_scan",
            results=Results(results=[], errors=[]),
            scans=[
                ScanCollection(
                    id="scan",
                    type="test",
                    results=Results(results=[result], errors=[]),
                    optional_header="> This is an example header",
                )
            ],
        )
    )

    incidents = json.loads(output)["scans"][0]["entities_with_incidents"][0][
        "incidents"
    ]
    # We can rely on the policy break type, since in this test there are 2 policy breaks,
    # and they are of different types
    incident_for_policy_break_type = {
        incident["type"]: incident for incident in incidents
    }

    for policy_break in known_policy_breaks:
        assert incident_for_policy_break_type[policy_break.break_type]["known_secret"]

    for policy_break in new_policy_breaks:
        assert (
            "known_secret"
            not in incident_for_policy_break_type[policy_break.break_type]
        )
