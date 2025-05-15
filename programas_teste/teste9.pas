program WhileOnlyComplex;
var
  a, b, c: integer;
  flag: boolean;
begin
  a := 0;
  b := 5;
  c := 2;
  flag := false;

  while (a < b) and not flag do
  begin
    a := a + 1;

    while (c < b) or flag do
    begin
      c := c + 1;
      flag := true;
    end;

    flag := false;
  end;
end.
