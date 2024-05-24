{
  inputs = {
    systems.url = "github:nix-systems/x86_64-linux";
    nixvim.url = "github:nix-community/nixvim";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      devShells = {
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
      };

      packages = {
        default = pkgs.python3.pkgs.buildPythonPackage rec {
          pname = "swwwmgr";
          version = "v0.1.2-alpha";

          src = pkgs.fetchFromGitHub {
            owner = "Kodlak15";
            repo = "swww-manager";
            rev = version;
            hash = "sha256-xwQnd2xivTVxns2YH/g+JPWqVVQykK9nx6DTr5CYv14=";
          };

          propagatedBuildInputs = with pkgs.python311Packages; [pyyaml];
        };
      };
    });
}
