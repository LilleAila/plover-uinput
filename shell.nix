{ pkgs ? import <nixpkgs> {} }: pkgs.mkShell {
  packages = with pkgs; [
    (python311.withPackages (ps: with ps; [
      evdev
      xkbcommon
      setuptools
      plover
    ]))
    black
    plover.dev
    # nodePackages.pyright # error where not supposed to error
  ];
}
