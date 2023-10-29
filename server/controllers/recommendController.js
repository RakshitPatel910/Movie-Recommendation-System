import { spawn } from "child_process"

export const getContentBasedRec = async (req, res) => {
    const { input_movies } = req.body

    // const input_movies = ['The Dark Knight Rises', 'The Avengers', 'Iron Man', 'Avatar', 'Life of Pi']
    // let input = JSON.parse(input_movies)
    try {
        const recommender = spawn('python', ['./python/getRecommendation.py'])

        recommender.stdin.write(JSON.stringify(input_movies));
        recommender.stdin.end();
        
        let recommendations;
        let recArray;

        recommender.stdout.on('data', async (data) => {
            recommendations = await data.toString();
            // recommendations = await data;
            recommendations = await recommendations.replaceAll("[", '');
            recommendations = await recommendations.replaceAll("]", '');
            recommendations = await recommendations.replaceAll("'", '');
            recommendations = await recommendations.replaceAll('"', '');
            recommendations = await recommendations.replaceAll(', ', ',');
            recommendations = await recommendations.replaceAll('\r\n', '');

            recArray = await recommendations.split(',');

            console.log(recArray);
        })

        recommender.on('close', (code) => {
            console.log(`Python script exited with code ${code}`)

            return res.json({ recommendationList: recArray })
        })
        
    } catch (error) {
        return res.json({ message: "Something went wrong.", error: error });
    }
}

