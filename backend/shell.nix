{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.virtualenv
    pkgs.python311Packages.sqlalchemy
    pkgs.python311Packages.pyodbc
    pkgs.unixODBC
    pkgs.msodbcsql18
  ];
}
