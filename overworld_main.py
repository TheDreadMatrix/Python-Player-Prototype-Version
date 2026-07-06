



def main():
    from supermarioworld.core.app import SuperMariWorldApplication


    smw = SuperMariWorldApplication(file_execution=__file__, use_resizeble=True, vendor_size=(1000, 700), title="SMW91: Overworld editor")
    smw._run_scene = "base:overworld-editor"
    smw.audio.setFilterLowPass(1500)
    smw._initSubstence()
    smw._run()
    



if __name__ == "__main__":
    main()
    print("FINISHED OK")