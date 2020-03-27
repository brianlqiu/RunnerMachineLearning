# Runner Machine Learning

An AI learning how to play a simplified version of my Runner game using the NEAT python module.

## Notes

In this version of Runner, the sign obstacles are removed and the AI is only trained to jump over the stump obstacles.

The AI tends to work best when obstacles are generated far enough apart so that excessive jumping is punished. 
Since the distance between obstacles is linked to the frame rate, the obstacle generation timing will have to be adjusted according to the
capabilities of every machine.
