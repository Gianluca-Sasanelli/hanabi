import { createDeck } from "@/lib/backend/startgameutils"
import { NextResponse } from "next/server"
import { v4 as uuidv4 } from "uuid"
import { ApiResponse } from "@/types/api"
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!)

export async function POST() {
  try {
    const deck = createDeck()
    const game_id = uuidv4()
    
    const { error: dbError } = await supabase
      .from('games')
      .insert([{ game_id, deck }])
    
    if (dbError) throw dbError
    
    const response: ApiResponse<{ game_id: string; deck: ReturnType<typeof createDeck> }> = {
      success: true,
      data: { game_id, deck: deck },
      error: null,
      meta: {
        timestamp: new Date().toISOString()
      }
    }
    
    return NextResponse.json(response)
  } catch (error) {
    console.error('Database error:', error)
    return NextResponse.json({
      success: false,
      data: null,
      error: "Failed to start game",
      meta: {
        timestamp: new Date().toISOString()
      }
    }, { status: 500 })
  }
}

