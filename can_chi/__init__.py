def can_chi(year: int) -> str:
    thien_can = ["Giáp", "Ất", "Bính", "Đinh", "Mậu",
                 "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    dia_chi = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
               "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

    can = thien_can[(year + 6) % 10]
    chi = dia_chi[(year + 8) % 12]
    return f"{can} {chi}"


if __name__ == '__main__':
    for y in [2026, 2027]:
        print(y, "=", can_chi(y))