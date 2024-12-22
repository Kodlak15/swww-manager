{
  lib,
  config,
  ...
}: let
  inherit (lib) mkOption types;
in {
  options.programs.swwwmgr = {
    enable = mkOption {
      type = types.bool;
      default = false;
      description = "Whether to enable swwwmgr";
    };
    transition = mkOption {
      type = types.attrs;
      default = {
        angle = "45";
        duration = "3";
        position = "center";
        step = "90";
        type = "fade";
      };
      description = "Transition configuration to be passed to swww";
    };
  };
  config = {
    "${config.xdg.configHome}/swwwmgr/config.yaml".text = ''
      transition:
        angle: ${config.programs.swwwmgr.transition.angle}
        duration: ${config.programs.swwwmgr.transition.duration}
        position: ${config.programs.swwwmgr.transition.position}
        step: ${config.programs.swwwmgr.transition.step}
        type: ${config.programs.swwwmgr.transition.type}
    '';
  };
}
