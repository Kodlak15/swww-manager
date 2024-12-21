{
  pkgs,
  lib,
  inputs,
  config,
  ...
}: let
  inherit (lib) mkOption types;
in {
  options.swwwmgr = {
    enable = mkOption {
      type = types.bool;
      default = false;
      description = "Whether to enable swwwmgr";
    };
    transition = mkOption {
      type = types.attrs;
      default = {
        angle = "180";
        duration = "0.5";
        position = "0.7,0.9";
        step = "180";
        type = "wipe";
      };
      description = "Transition configuration to be passed toswww";
    };
  };
}
