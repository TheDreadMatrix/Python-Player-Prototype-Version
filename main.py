



def main():
    from supermarioworld.core.app import SuperMariWorldApplication


    smw = SuperMariWorldApplication(__file__)    
    smw._initSubstence()

    try:
        smw._run()
        print("FINISHED OK")
    except KeyboardInterrupt:
        print("FINISHED INTERRUPTED")
    



if __name__ == "__main__":
    main()
    