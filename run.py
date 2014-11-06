"""
External endpoint to the duel package.
This has to be run from one level outside the package
"""

from duel import app

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()