{ pkgs ? import <nixpkgs> {} }: pkgs.mkShell {
  packages = with pkgs; [
    (python311.withPackages (ps: with ps; [
      evdev
      xkbcommon
      setuptools
    ]))
    black
    # nodePackages.pyright # error where not supposed to error
  ];
}
