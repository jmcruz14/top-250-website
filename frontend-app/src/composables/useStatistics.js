import * as d3 from 'd3'
import { chain, isNull } from 'lodash'

export const useStatistics = () => {
  // ensure functions added here pertain to stat calculations only

  /**
   * Parses the resulting list of movies and retrieves
   * the top five most reviewed films according to the database.
   * 
   * @param {Object} data 
   * @returns {Array<Object>}
   */
  function mostReviewed (data) {
    const reviewCount = chain(data)
      .filter(i => i?.review_count)
      .value()
    const sortedReviewCount = reviewCount.slice().sort((a, b) => d3.descending(a.review_count, b.review_count));
    const topFive = sortedReviewCount.slice(0,5)
    return topFive
  }

  /**
   * Parses the resulting list of movies and retrieves
   * the top five most viewed films.
   * 
   * @param {Object} data 
   * @returns {Array<Object>}
   */
  function mostViewed (data) {
    const viewCount = chain(data)
      .filter(i => i?.watch_count)
      .value()
    const sortedViewCount = viewCount.slice().sort((a, b) => d3.descending(a.watch_count, b.watch_count))
    const topFive = sortedViewCount.slice(0,5)
    return topFive
  }

  function mostLiked (data) {
    const likeCount = chain(data)
      .filter(i => i?.like_count)
      .value()
    const sortedLikeCount = likeCount.slice().sort((a, b) => d3.descending(a.like_count, b.like_count));
    const topFive = sortedLikeCount.slice(0, 5);
    return topFive
  }

  /**
   * Gets the statistical count of unrated movies in the list
   * and additional metadata
   * 
   * @param {Object} data 
   * @returns {Number}
   */
  function unratedMovies (data) {
    const unrated = chain(data)
      .filter(i => isNull(i.rating))
      .value()
    
    const avgRating = unrated?.reduce((a, movie) => {
      const classic_rating = movie?.classic_rating
      return a + classic_rating
    }, 0) / unrated?.length

    const avgWatchCount = unrated?.reduce((a, movie) => {
      const watch_count = movie?.watch_count
      return a + watch_count
    }, 0) / unrated?.length

    return {
      'films': unrated,
      'count': unrated?.length,
      'average_rating': avgRating,
      'average_watch_count': avgWatchCount
    }
  }

  /**
   * Gets the statistical count of rated movies in the list
   * and additional metadata
   * 
   * @param {Object} data 
   * @returns {Number}
   */
  function ratedMovies (data) {
    const rated = chain(data)
      .filter(i => i?.rating)
      .value()
    
    const avgRating = rated?.reduce((a, movie) => {
      const classic_rating = movie?.classic_rating
      return a + classic_rating
    }, 0) / rated?.length

    const avgWatchCount = rated?.reduce((a, movie) => {
      const watch_count = movie?.watch_count
      return a + watch_count
    }, 0) / rated?.length

    return {
      'films': rated,
      'count': rated?.length,
      'average_rating': avgRating,
      'average_watch_count': avgWatchCount
    }
  }

  // PUT THRU AGGREGATE FUNCTION
  // function perDecade (data) {
  //   const decadeThresholds = d3.bin().thresholds([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030]);
  //   const years = data.map(d => d.)
  // }

  return {
    mostReviewed,
    mostViewed,
    mostLiked,
    unratedMovies,
    ratedMovies,
  }
}