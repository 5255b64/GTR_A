# TODO 重构

from src.utils import sub_call_hook, file_helper
from src.CONFIG import JACOCOCLI_JAR_ADDR, JVM


def run(report_file_path: str, class_file_path: str, source_file: str, output_html_path: str):
    file_helper.check_path_exists(output_html_path)

    cmd = [
        JVM,
        "-jar", JACOCOCLI_JAR_ADDR,
        "report", report_file_path,
        "--classfiles", class_file_path,
        "--sourcefiles", source_file,
        "--html", output_html_path,
    ]
    # print(" ".join(cmd))
    # sub_call_hook.serial(" ".join(cmd))
    sub_call_hook.serial_stderr(cmd)


if __name__ == "__main__":
    run(
        report_file_path="/tmp/tmp_root_folder/xxx/test_dest/right_dest.exec",
        class_file_path="/tmp/tmp_root_folder/xxx/tmp/tmp_Time_1/tmp_step2/checkout/build/classes",
        source_file="/tmp/tmp_root_folder/xxx/tmp/tmp_Time_1/tmp_step2/checkout/src",
        output_html_path="/tmp/tmp_root_folder/xxx/test_dest/dest_output_false",

        # report_file_path="/tmp/tmp_root_folder/xxx/test_dest/false_dest.exec",
        # class_file_path="/tmp/tmp_root_folder/xxx/tmp/tmp_Time_12/tmp_step2/checkout/build/classes",
        # source_file="/tmp/tmp_root_folder/xxx/tmp/tmp_Time_12/tmp_step2/checkout/src",
        # output_html_path="/tmp/tmp_root_folder/xxx/test_dest/dest_output_false",
    )
