{
  description = "A rudimentary image management script build on top of swww.";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs @ {
    self,
    flake-parts,
    ...
  }: let
    pkgs = import inputs.nixpkgs {system = "x86_64-linux";};
  in
    flake-parts.lib.mkFlake {inherit inputs;} {
      imports = [
        ./modules/home-manager
      ];
      systems = ["x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin"];
      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        ...
      }: {};
      flake = {
        devShells = {
          "x86_64-linux".default = pkgs.mkShell {
            packages = with pkgs; [
              python312Packages.pyyaml
              python312Packages.setuptools
            ];
          };
        };
        packages = {
          "x86_64-linux".default = pkgs.python3.pkgs.buildPythonPackage {
            pname = "swwwmgr";
            version = "v0.1.2-alpha";
            src = ./.;
            propagatedBuildInputs = with pkgs.python312Packages; [pyyaml];
          };
        };
        homeManagerModules.default = import ./modules/home-manager;
      };
    };
}
