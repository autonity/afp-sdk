{
  config,
  ...
}:

{
  env.UV_PYTHON = "${config.env.DEVENV_PROFILE}/bin/python";

  languages.python = {
    enable = true;
    version = "3.13";
    uv.enable = true;
    uv.sync.enable = true;
    uv.sync.groups = [ "dev" ];
    venv.enable = false;
  };

  # See full reference at https://devenv.sh/reference/options/
}
