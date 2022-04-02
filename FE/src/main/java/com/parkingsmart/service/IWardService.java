package com.parkingsmart.service;

import java.util.List;

import com.parkingsmart.dto.WardDTO;

public interface IWardService {
	public List<WardDTO> findByDistrict(String id);
	public WardDTO findOneById(String id);
}
