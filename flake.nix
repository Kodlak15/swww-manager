{
  description = "Command line utility script for managing wallpaper with swww (https://github.com/LGFae/swww)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forEachSupportedSystem = f:
      nixpkgs.lib.genAttrs supportedSystems (system:
        f {
          pkgs = import nixpkgs {inherit system;};
        });
  in {
    devShells = forEachSupportedSystem ({pkgs}: {
      default = pkgs.mkShell {
        packages = [
          (pkgs.python3.withPackages (python-pkgs: [
            # Add packages here
            python-pkgs.ipython
            python-pkgs.pyyaml
            python-pkgs.setuptools
          ]))
        ];

        shellHook = ''
          exec $SHELL;
        '';
      };
    });

    packages = forEachSupportedSystem ({pkgs}: {
      default = pkgs.python3.pkgs.buildPythonPackage rec {
        pname = "swwwmgr";
        version = "v0.1.0-alpha";

        src = pkgs.fetchFromGitHub {
          owner = "Kodlak15";
          repo = "swww-manager";
          rev = version;
          hash = "sha256-4iJIzmHBJvRcz4aWqSAGHfYrCIi6v/PNF2ejgJ7LMJw=";
        };

        propagatedBuildInputs = with pkgs.python311Packages; [pyyaml];
      };
    });
  };
}
