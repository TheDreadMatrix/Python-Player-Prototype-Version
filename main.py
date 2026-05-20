



def main():
    from supermarioworld.core.smwkernel import SuperMariWorldApplication


    smw = SuperMariWorldApplication(__file__)
    smw._run()
    



if __name__ == "__main__":
    main()
    print("FINISHED OK")