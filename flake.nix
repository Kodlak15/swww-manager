{
  description = "A rudimentary image management script build on top of swww.";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs @ {flake-parts, ...}:
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
      }: {
        pkgs = import inputs.nixpkgs {inherit system;};
      };
      flake = {
        packages = {
          default = inputs.nixpkgs.python3.pkgs.buildPythonPackage {
            pname = "swwwmgr";
            src = ./.;
            # version = "v0.1.2-alpha";
            # src = inputs.nixpkgs.fetchFromGitHub {
            #   owner = "Kodlak15";
            #   repo = "swww-manager";
            #   rev = version;
            #   hash = "sha256-xwQnd2xivTVxns2YH/g+JPWqVVQykK9nx6DTr5CYv14=";
            # };
            propagatedBuildInputs = with inputs.nixpkgs.python311Packages; [pyyaml];
          };
        };
      };
    };
}
