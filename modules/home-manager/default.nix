self: {
  pkgs,
  lib,
  config,
  ...
}: let
  inherit (lib) mkEnableOption mkOption mkIf types;
  inherit (pkgs.stdenv.hostPlatform) system;
  cfg = config.programs.swwwmgr;
  package = self.packages.${system}.default;
in {
  imports = [];

  options.programs.swwwmgr = {
    enable = mkEnableOption "swwwmgr";
    package = mkOption {
      type = types.package;
      default = package;
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
    hooks = mkOption {
      type = types.attrs;
      default = {};
      example = {
        after_set = [
          "wal -i {image}"
        ];
      };
      description = "Hooks to be executed after the wallpaper is set";
    };
  };

  config = mkIf cfg.enable {
    home.packages = [cfg.package];
    xdg.configFile."swwwmgr/config.yaml".text = ''
      transition:
        angle: ${cfg.transition.angle}
        duration: ${cfg.transition.duration}
        position: ${cfg.transition.position}
        step: ${cfg.transition.step}
        type: ${cfg.transition.type}
      hooks:
        after_set:
          ${lib.concatMapStrings (hook: "- ${hook}\n") cfg.hooks.after_set}
    '';
  };
}
