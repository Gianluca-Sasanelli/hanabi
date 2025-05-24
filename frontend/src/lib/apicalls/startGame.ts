import { Card } from '@/types/hanabi';
import { apiRequest } from './baseApi'
import { Result } from '@/types/apiTypes'
import { useCardStore } from '@/store/CardStore';
export interface SegmentResponse {
  image_blob_name: string | string[]
}
const backend = "http://localhost:8000"
interface StartGameResponnse {
    game_id: string;
    deck: Card[];
}
export async function startGame(): Promise<Result<StartGameResponnse>> {
    const response = await apiRequest<StartGameResponnse>(`${backend}/game/start_game`, {
        method: 'POST',

    })
    if (response.success) {
        const { deck } = response.data;
        useCardStore.getState().setCardData(deck);
    }
    return response
}
