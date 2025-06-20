"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Upload, Play, Sparkles, Users, Video, ArrowRight, Check, X } from "lucide-react"

type Character = {
  name: string
  avatar?: File
  traits: string[]
}

type Step = "landing" | "story" | "characters" | "video"

const adjectives = [
  "Brave",
  "Mysterious",
  "Cheerful",
  "Wise",
  "Adventurous",
  "Gentle",
  "Fierce",
  "Curious",
  "Loyal",
  "Witty",
  "Compassionate",
  "Bold",
  "Clever",
  "Graceful",
  "Determined",
  "Playful",
  "Noble",
  "Mischievous",
  "Confident",
  "Humble",
  "Energetic",
  "Calm",
  "Ambitious",
  "Kind",
]

export default function TellMeYourStory() {
  const [currentStep, setCurrentStep] = useState<Step>("landing")
  const [story, setStory] = useState("")
  const [characters, setCharacters] = useState<Character[]>([])
  const [videoProgress, setVideoProgress] = useState(0)
  const [videoGenerated, setVideoGenerated] = useState(false)

  const countSentences = (text: string) => {
    return text.split(/[.!?]+/).filter((sentence) => sentence.trim().length > 0).length
  }

  const extractCharacters = (storyText: string): Character[] => {
    // Simulate character extraction - in real app this would use AI
    const commonNames = ["Alex", "Sarah", "John", "Emma", "Michael", "Lisa", "David", "Anna"]
    const foundNames = commonNames.filter((name) => storyText.toLowerCase().includes(name.toLowerCase()))

    // Add some random characters if none found
    if (foundNames.length === 0) {
      foundNames.push("Main Character", "Supporting Character")
    }

    return foundNames.slice(0, 4).map((name) => ({ name, traits: [] }))
  }

  const handleStorySubmit = () => {
    const extractedCharacters = extractCharacters(story)
    setCharacters(extractedCharacters)
    setCurrentStep("characters")
  }

  const handleCharacterUpdate = (index: number, field: keyof Character, value: any) => {
    const updated = [...characters]
    if (field === "traits") {
      const currentTraits = updated[index].traits
      if (currentTraits.includes(value)) {
        updated[index].traits = currentTraits.filter((trait) => trait !== value)
      } else {
        updated[index].traits = [...currentTraits, value]
      }
    } else {
      updated[index] = { ...updated[index], [field]: value }
    }
    setCharacters(updated)
  }

  const handleAvatarUpload = (index: number, file: File) => {
    handleCharacterUpdate(index, "avatar", file)
  }

  const generateVideo = () => {
    setCurrentStep("video")
    setVideoProgress(0)

    // Simulate video generation progress
    const interval = setInterval(() => {
      setVideoProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setVideoGenerated(true)
          return 100
        }
        return prev + 10
      })
    }, 500)
  }

  const sentenceCount = countSentences(story)
  const isStoryValid = story.trim().length > 0 && sentenceCount <= 30

  if (currentStep === "landing") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100">
        {/* Header */}
        <header className="px-4 lg:px-6 h-16 flex items-center border-b bg-white/80 backdrop-blur-sm">
          <div className="flex items-center space-x-2">
            <Video className="h-8 w-8 text-purple-600" />
            <span className="text-xl font-bold text-gray-900">Tell Me Your Story</span>
          </div>
          <nav className="ml-auto flex gap-4 sm:gap-6">
            <Button variant="ghost" onClick={() => setCurrentStep("story")}>
              Get Started
            </Button>
          </nav>
        </header>

        {/* Hero Section */}
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6 mx-auto">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                    Transform Your Stories Into Stunning Videos
                  </h1>
                  <p className="max-w-[600px] text-gray-600 md:text-xl">
                    Share your ideas, stories, and imagination. Our AI will bring them to life with personalized
                    characters and cinematic visuals.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button
                    size="lg"
                    onClick={() => setCurrentStep("story")}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  >
                    Start Creating <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="lg">
                    Watch Demo
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <div className="relative">
                  <div className="w-80 h-80 bg-gradient-to-br from-purple-400 to-blue-500 rounded-3xl flex items-center justify-center">
                    <Play className="h-20 w-20 text-white" />
                  </div>
                  <div className="absolute -top-4 -right-4 w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center">
                    <Sparkles className="h-8 w-8 text-yellow-800" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-white">
          <div className="container px-4 md:px-6 mx-auto">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">How It Works</h2>
                <p className="max-w-[900px] text-gray-600 md:text-xl/relaxed">
                  Three simple steps to transform your story into a captivating video
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3 lg:gap-12">
              <Card className="text-center">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                    <span className="text-xl font-bold text-purple-600">1</span>
                  </div>
                  <CardTitle>Share Your Story</CardTitle>
                  <CardDescription>Write your story, idea, or script in up to 30 sentences</CardDescription>
                </CardHeader>
              </Card>
              <Card className="text-center">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                    <Users className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle>Customize Characters</CardTitle>
                  <CardDescription>Upload avatars and define personality traits for your characters</CardDescription>
                </CardHeader>
              </Card>
              <Card className="text-center">
                <CardHeader>
                  <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                    <Video className="h-6 w-6 text-green-600" />
                  </div>
                  <CardTitle>Watch Your Video</CardTitle>
                  <CardDescription>Our AI generates a stunning video bringing your story to life</CardDescription>
                </CardHeader>
              </Card>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-r from-purple-600 to-blue-600">
          <div className="container px-4 md:px-6 mx-auto">
            <div className="flex flex-col items-center justify-center space-y-4 text-center text-white">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">Ready to Bring Your Story to Life?</h2>
                <p className="max-w-[600px] text-purple-100 md:text-xl/relaxed">
                  Join thousands of creators who have transformed their ideas into amazing videos
                </p>
              </div>
              <Button
                size="lg"
                variant="secondary"
                onClick={() => setCurrentStep("story")}
                className="bg-white text-purple-600 hover:bg-gray-100"
              >
                Start Creating Now <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        </section>
      </div>
    )
  }

  if (currentStep === "story") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 p-4">
        <div className="max-w-4xl mx-auto py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Tell Me Your Story</h1>
            <p className="text-gray-600">Share your story in up to 30 sentences</p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Your Story</CardTitle>
              <CardDescription>
                Write your story, idea, or script. Our AI will identify characters and bring your narrative to life.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Textarea
                  placeholder="Once upon a time, in a magical kingdom far away..."
                  value={story}
                  onChange={(e) => setStory(e.target.value)}
                  className="min-h-[300px] text-base"
                />
                <div className="flex justify-between items-center mt-2 text-sm">
                  <span className={`${sentenceCount > 30 ? "text-red-500" : "text-gray-500"}`}>
                    {sentenceCount}/30 sentences
                  </span>
                  {sentenceCount > 30 && (
                    <span className="text-red-500 flex items-center">
                      <X className="h-4 w-4 mr-1" />
                      Too many sentences
                    </span>
                  )}
                </div>
              </div>

              <div className="flex gap-4">
                <Button variant="outline" onClick={() => setCurrentStep("landing")}>
                  Back
                </Button>
                <Button
                  onClick={handleStorySubmit}
                  disabled={!isStoryValid}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  Continue to Characters <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (currentStep === "characters") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 p-4">
        <div className="max-w-6xl mx-auto py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">Customize Your Characters</h1>
            <p className="text-gray-600">Upload avatars and define personality traits for each character</p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
            {characters.map((character, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-lg">{character.name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor={`avatar-${index}`}>Avatar (Optional)</Label>
                    <div className="mt-2">
                      <Input
                        id={`avatar-${index}`}
                        type="file"
                        accept="image/*"
                        onChange={(e) => {
                          const file = e.target.files?.[0]
                          if (file) handleAvatarUpload(index, file)
                        }}
                        className="hidden"
                      />
                      <Button
                        variant="outline"
                        onClick={() => document.getElementById(`avatar-${index}`)?.click()}
                        className="w-full"
                      >
                        <Upload className="h-4 w-4 mr-2" />
                        {character.avatar ? "Change Avatar" : "Upload Avatar"}
                      </Button>
                      {character.avatar && (
                        <p className="text-sm text-green-600 mt-1 flex items-center">
                          <Check className="h-4 w-4 mr-1" />
                          Avatar uploaded
                        </p>
                      )}
                    </div>
                  </div>

                  <div>
                    <Label>Personality Traits</Label>
                    <div className="mt-2 grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
                      {adjectives.map((trait) => (
                        <Button
                          key={trait}
                          variant={character.traits.includes(trait) ? "default" : "outline"}
                          size="sm"
                          onClick={() => handleCharacterUpdate(index, "traits", trait)}
                          className="text-xs"
                        >
                          {trait}
                        </Button>
                      ))}
                    </div>
                    {character.traits.length > 0 && (
                      <p className="text-sm text-gray-600 mt-2">Selected: {character.traits.join(", ")}</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="flex gap-4 justify-center">
            <Button variant="outline" onClick={() => setCurrentStep("story")}>
              Back to Story
            </Button>
            <Button
              onClick={generateVideo}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
            >
              Generate Video <Video className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    )
  }

  if (currentStep === "video") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 p-4">
        <div className="max-w-4xl mx-auto py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">
              {videoGenerated ? "Your Video is Ready!" : "Generating Your Video..."}
            </h1>
            <p className="text-gray-600">
              {videoGenerated
                ? "Your story has been transformed into an amazing video"
                : "Our AI is creating your personalized video"}
            </p>
          </div>

          <Card>
            <CardContent className="p-8">
              {!videoGenerated ? (
                <div className="space-y-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Sparkles className="h-8 w-8 text-white animate-pulse" />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">Creating Magic...</h3>
                    <p className="text-gray-600">This usually takes 2-3 minutes</p>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{videoProgress}%</span>
                    </div>
                    <Progress value={videoProgress} className="w-full" />
                  </div>

                  <div className="text-sm text-gray-600 space-y-1">
                    <p>✓ Analyzing your story</p>
                    <p>✓ Processing characters</p>
                    <p className={videoProgress > 50 ? "" : "opacity-50"}>
                      {videoProgress > 50 ? "✓" : "○"} Generating scenes
                    </p>
                    <p className={videoProgress > 80 ? "" : "opacity-50"}>
                      {videoProgress > 80 ? "✓" : "○"} Adding final touches
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="aspect-video bg-gradient-to-br from-gray-900 to-gray-700 rounded-lg flex items-center justify-center">
                    <div className="text-center text-white">
                      <Play className="h-16 w-16 mx-auto mb-4" />
                      <p className="text-lg">Your Generated Video</p>
                      <p className="text-sm opacity-75">Click to play</p>
                    </div>
                  </div>

                  <div className="flex gap-4 justify-center">
                    <Button variant="outline">Download Video</Button>
                    <Button variant="outline">Share Video</Button>
                    <Button
                      onClick={() => {
                        setCurrentStep("story")
                        setStory("")
                        setCharacters([])
                        setVideoProgress(0)
                        setVideoGenerated(false)
                      }}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                      Create Another Video
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return null
}
