



def main():
    from supermarioworld.core.app import SuperMariWorldApplication


    smw = SuperMariWorldApplication(__file__)
    smw._DEBUG = True
    smw._initSubstence()
    smw._run()
    



if __name__ == "__main__":
    main()
    print("FINISHED OK")