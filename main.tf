module "lambda-package" {
  source = "github.com/af6140/terraform-package-lambda?ref=v0.1.0"
  #source = "../terraform-package-lambda/"
  code = "lambdas/test_logging/test_logging.py"

  /* Optional, defaults to the value of $code, except the extension is
   * replaced with ".zip" */
  output_filename = "tmp/test_logging.zip"

  /* Optional, specifies additional files to include.  These are relative
   * to the location of the code. */
  extra_files = [  ]
}

# resource "aws_lambda_function" "my_lambda" {
#   /* ... */
#   filename = "${module.lambda-package.output_filename}"
#   source_code_hash = "${module.lambda-package.output_base64sha256}"
#   /* ... */
# }