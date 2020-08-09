def futoshiki_to_html(futoshiki_board, filename='../futoshiki.html'):
    with open(filename, 'w') as file:
        file.write('''<style>
            table, tr, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 20px;
            font-size: 20px;
            font-family: monospace;
            text-align: center;
        }
        
        tr, td {
            width: 23px;
            height: 64px;
        }
        
        table {
            margin-left: auto;
            margin-right: auto;
            margin-top: 30px;
        }
        
        </style>
        <table>''')
        for tr in range(len(futoshiki_board)):
            file.write('<tr>')
            for td in range(len(futoshiki_board[tr])):
                file.write(
                    f'<td style="{"background-color: lavender;" if futoshiki_board[tr][td].has_constraints() else ""}"'
                    f'>{futoshiki_board[tr][td] if futoshiki_board[tr][td].value != 0 else ""}</td>')
            file.write('</tr>')
        file.write('</table>')


def skyscrapper_to_html(skyscrapper_board, constraints):
    with open('../skyscrapper.html', 'w') as file:
        file.write('''<style>
            table, tr, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 20px;
            font-size: 20px;
            font-family: monospace;
            text-align: center;
        }

        tr, td {
            width: 23px;
            height: 64px;
        }

        table {
            margin-left: auto;
            margin-right: auto;
            margin-top: 30px;
        }

        </style>
        <table>''')
        for tr in range(len(skyscrapper_board) + 2):
            if tr == 0:
                file.write(f'<td style="border-left-color: white; border-top-color: white;"></td>')
                for i in range(len(constraints['G'])):
                    file.write(
                        f'<td style="background-color: lightgreen;"><b>{constraints["G"][i] if constraints["G"][i] != 0 else ""}</b></td>')
                file.write(f'<td style="border-top-color: white; border-right-color: white;"></td>')
            elif tr == len(skyscrapper_board) + 1:
                file.write(f'<td style="border-left-color: white; border-bottom-color: white;"></td>')
                for i in range(len(constraints['D'])):
                    file.write(
                        f'<td style="background-color: lightgreen;"><b>{constraints["D"][i] if constraints["D"][i] != 0 else ""}</b></td>')
                file.write(f'<td style="border-right-color: white; border-bottom-color: white;"></td>')
            else:
                file.write('<tr>')
                for td in range(len(skyscrapper_board[tr - 1]) + 2):
                    if td == 0:
                        file.write(
                            f'<td style="background-color: lightgreen;"><b>{constraints["L"][tr - 1] if constraints["L"][tr - 1] != 0 else ""}</b></td>')
                    elif td == len(skyscrapper_board[tr - 1]) + 1:
                        file.write(
                            f'<td style="background-color: lightgreen;"><b>{constraints["P"][tr - 1] if constraints["P"][tr - 1] != 0 else ""}</b></td>')
                    else:
                        file.write(
                            f'<td>{skyscrapper_board[tr - 1][td - 1] if skyscrapper_board[tr - 1][td - 1] != 0 else ""}</td>')
                file.write('</tr>')
        file.write('</table>')
