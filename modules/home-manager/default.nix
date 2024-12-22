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
    package = mkOption {
      type = types.package;
      default = self.packages."x86_64-linux".swwwmgr;
      description = "The swwwmgr package to use";
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
  config = lib.mkIf config.programs.swwwmgr.enable {
    home.file.".config/swwwmgr/config.yaml".text = ''
      transition:
        angle: ${config.programs.swwwmgr.transition.angle}
        duration: ${config.programs.swwwmgr.transition.duration}
        position: ${config.programs.swwwmgr.transition.position}
        step: ${config.programs.swwwmgr.transition.step}
        type: ${config.programs.swwwmgr.transition.type}
    '';
  };
}
