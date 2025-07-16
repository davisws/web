from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Lawn & Labor Solutions</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-green-50 text-gray-800 font-sans scroll-smooth">

      <!-- Navbar -->
      <nav class="bg-green-800 text-white px-6 py-4 sticky top-0 shadow z-50">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
          <h1 class="text-xl font-bold">Lawn & Labor Solutions</h1>
          <ul class="flex space-x-6 text-sm">
            <li><a href="#home" class="hover:underline">Home</a></li>
            <li><a href="#plans" class="hover:underline">Plans</a></li>
            <li><a href="#services" class="hover:underline">Services</a></li>
            <li><a href="#team" class="hover:underline">Team</a></li>
            <li><a href="#contact" class="hover:underline">Contact</a></li>
          </ul>
        </div>
      </nav>

      <!-- Hero Section -->
      <section id="home" class="bg-green-100 py-16 text-center">
        <h2 class="text-4xl font-bold mb-4">Welcome to Lawn & Labor Solutions</h2>
        <p class="text-lg max-w-xl mx-auto">Providing reliable, affordable yard care and labor services tailored to your needs.</p>
      </section>

      <!-- Plans Section -->
      <section id="plans" class="max-w-6xl mx-auto p-6">
        <h2 class="text-3xl font-semibold mb-6 text-center">Service Plans</h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="border rounded-xl p-4 bg-white shadow">
            <h3 class="text-xl font-bold mb-2">Basic Plan</h3>
            <p class="text-sm text-gray-600 mb-2">Starting at $40/week (based on yard size)</p>
            <ul class="list-disc ml-5">
              <li>Mowing</li>
              <li>Blowing</li>
            </ul>
          </div>
          <div class="border rounded-xl p-4 bg-white shadow">
            <h3 class="text-xl font-bold mb-2">Standard Plan</h3>
            <p class="text-sm text-gray-600 mb-2">Starting at $55/week</p>
            <ul class="list-disc ml-5">
              <li>Mowing</li>
              <li>Edging</li>
              <li>Trimming</li>
              <li>Blowing</li>
            </ul>
          </div>
          <div class="border rounded-xl p-4 bg-white shadow">
            <h3 class="text-xl font-bold mb-2">Premium Plan</h3>
            <p class="text-sm text-gray-600 mb-2">Starting at $70/week</p>
            <ul class="list-disc ml-5">
              <li>Mowing</li>
              <li>Edging</li>
              <li>Trimming</li>
              <li>Monthly Fertilizing</li>
              <li>Flower Bed Weeding</li>
              <li>Blowing</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Extra Services -->
      <section id="services" class="bg-white py-12">
        <div class="max-w-5xl mx-auto px-6">
          <h2 class="text-3xl font-semibold mb-6 text-center">Additional Services</h2>
          <ul class="grid md:grid-cols-2 gap-4 list-disc ml-5">
            <li>Window Washing - Crystal clear results inside &amp; out</li>
            <li>Ditch Bank Burning - Safe controlled cleanup of overgrowth</li>
            <li>Yard Clean-Up - Debris removal and seasonal leaf cleanup</li>
            <li>Tree Trimming - Shaping, pruning, and branch removal</li>
          </ul>
        </div>
      </section>

      <!-- Team Section -->
      <section id="team" class="bg-green-100 py-12">
        <div class="max-w-5xl mx-auto text-center px-6">
          <h2 class="text-3xl font-semibold mb-6">Meet the Team</h2>
          <div class="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div>
              <img src="https://via.placeholder.com/150" alt="Team Member" class="rounded-full mx-auto mb-2"/>
              <h3 class="font-bold">David</h3>
              <p class="text-sm text-gray-600">Owner &amp; Lead Laborer</p>
            </div>
            <div>
              <img src="https://via.placeholder.com/150" alt="Team Member" class="rounded-full mx-auto mb-2"/>
              <h3 class="font-bold">Chris</h3>
              <p class="text-sm text-gray-600">Yard Tech &amp; Tree Trimmer</p>
            </div>
            <div>
              <img src="https://via.placeholder.com/150" alt="Team Member" class="rounded-full mx-auto mb-2"/>
              <h3 class="font-bold">Sarah</h3>
              <p class="text-sm text-gray-600">Customer Service</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Contact -->
      <section id="contact" class="bg-white py-12 text-center">
        <h2 class="text-3xl font-semibold mb-4">Let&apos;s Get to Work!</h2>
        <p class="text-lg mb-2">Text or Call us at:</p>
        <p class="text-green-700 text-2xl font-bold mb-4">208-241-1024</p>
        <p class="text-yellow-600 font-semibold">First mow only $25!</p>
      </section>

      <!-- Footer -->
      <footer class="bg-green-800 text-white text-center py-4">
        <p>&copy; 2025 Lawn & Labor Solutions. All rights reserved.</p>
      </footer>

    </body>
    </html>
    """
