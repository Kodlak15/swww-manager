{
  self,
  lib,
  config,
  ...
}: let
  inherit (lib) mkEnableOption mkOption mkIf types;
  cfg = config.programs.swwwmgr;
in {
  options.programs.swwwmgr = {
    enable = mkEnableOption "swwwmgr";
    package = mkOption {
      type = types.package;
      default = self.packages.swwwmgr;
      defaultText = literalExpression "pkgs.swwwmgr";
      description = ''
        The swwwmgr package to install.
      '';
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
  config = mkIf cfg.enable {
    home.packages = [cfg.package];
    xdg.configFile.".config/swwwmgr/config.yaml".text = ''
      transition:
        angle: ${cfg.transition.angle}
        duration: ${cfg.transition.duration}
        position: ${cfg.transition.position}
        step: ${cfg.transition.step}
        type: ${cfg.transition.type}
    '';
  };
}
