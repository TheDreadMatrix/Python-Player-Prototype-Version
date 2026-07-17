



def main():
    from supermarioworld.core.app import SuperMariWorldApplication
    import supermarioworld_config.scenes

    supermarioworld_config.scenes.START_SCENE = "base:overworld-editor"


    smw = SuperMariWorldApplication(__file__, project_name="supermarioworld_config", use_resizeble=True, vendor_size=(1000, 700), title="SMW91: Overworld editor")

    smw.audio.setFilterLowPass(1500)

    smw._run()
    



if __name__ == "__main__":
    main()
    print("FINISHED OK")