package com.smartparking.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartparking.dto.ProvinceDTO;
import com.smartparking.entity.ProvinceEntity;
import com.smartparking.mapper.ProvinceMapper;
import com.smartparking.repository.ProvinceRepository;
import com.smartparking.service.IProvinceService;

@Service
public class ProvinceService implements IProvinceService {
	
	@Autowired
	private ProvinceRepository repo;
	
	@Autowired
	private ProvinceMapper mapper;

	@Override
	public List<ProvinceDTO> findAll() {
		List<ProvinceEntity> list = repo.findAll();
		List<ProvinceDTO> results = new ArrayList<ProvinceDTO>();
		
		for (ProvinceEntity item : list) {
			results.add(mapper.ToDTO(item));
		}
		return results.isEmpty()?null:results;
	}

	@Override
	public ProvinceDTO findOneById(String id) {
		Optional<ProvinceEntity> province = repo.findById(id);
		if (province.isPresent()) {
			return mapper.ToDTO(province.get());
		}
		return null;
	}

}
