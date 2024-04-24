# Cantor<img src="images/icon.png" width="5%">: Inspiring Multimodal Chain-of-Thought of MLLM
[Project Home](https://ggg0919.github.io/cantor/)
<!-- <p align="center">
  <a href="https://ggg0919.github.io/cantor/">Project Home</a>
</p> -->

<!-- [Read our arXiv Paper]() -->

We propose an inspiring multimodal CoT framework named Cantor, which features a perceptual decision architecture that effectively integrates visual context and logical reasoning to solve visual reasoning tasks.

<p align="center" width="100%">
<a ><img src="images/fig2.png" alt="overview" style="width: 100%; min-width: 300px; display: block; margin: auto;"></a>
</p>


## Getting Started
**1. Installation**

Git clone our repository and creating Gemini environment:
```
git clone https://github.com/ggg0919/cantor
cd cantor
pip install -q -U google-generativeai
```

**2. Run Cantor Demo**

```
python3 demo.py --query "Which month is the hottest on average in Detroit?" --image_path ./images/image.png --api_key "your Gemini's key"
```
```--query```: Quetion  <br>
```--image_path```: Image path  <br>
```--api_key```: Your Gemini key  <br>

## ToDo
- [ ] Release the data and evaluation code on ScienceQA.
- [ ] Release the data and evaluation code on MathVista.

<!-- ## Citation
Please consider citing our paper if you think our codes, data, or models are useful. Thank you!
```

``` -->
